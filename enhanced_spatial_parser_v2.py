import pdfplumber
import re
from typing import Dict, List, Any, Tuple
import logging

logger = logging.getLogger(__name__)

class SimplifiedSpatialParser:
    """
    Simplified spatial parser that enhances the standard parser output
    instead of completely replacing it. Focuses on fixing action/dialogue spacing.
    """

    def __init__(self):
        # Tolerance settings for enhanced processing
        self.SPATIAL_CONFIG = {
            'x_tolerance': 3,      # Slightly more tolerant for real-world PDFs
            'y_tolerance': 4,      # Line grouping precision
            'layout': True         # Enable layout preservation
        }

    def enhance_standard_parser_output(self, pdf_path: str, standard_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance the standard parser output using spatial awareness
        """
        logger.info(f"🎯 Enhancing standard parser output with spatial analysis: {pdf_path}")

        try:
            with pdfplumber.open(pdf_path) as pdf:
                # Get enhanced scene content using spatial analysis
                enhanced_scenes = []

                for i, scene in enumerate(standard_result.get('scenes', [])):
                    logger.info(f"🔍 Enhancing scene {i+1}: {scene.get('heading', 'No heading')[:50]}...")

                    enhanced_content = self._enhance_scene_content_spatially(
                        pdf, scene.get('content', ''), scene.get('heading', '')
                    )

                    enhanced_scene = {
                        'heading': scene.get('heading', ''),
                        'content': enhanced_content,
                        'characters': scene.get('characters', [])
                    }
                    enhanced_scenes.append(enhanced_scene)

                # Update the result with enhanced scenes
                enhanced_result = standard_result.copy()
                enhanced_result['scenes'] = enhanced_scenes
                enhanced_result['metadata']['processedVia'] = 'railway-spatial-enhanced'

                logger.info(f"✅ Enhanced {len(enhanced_scenes)} scenes with spatial analysis")
                return enhanced_result

        except Exception as e:
            logger.error(f"❌ Spatial enhancement failed: {e}")
            # Return original result if enhancement fails
            return standard_result

    def _enhance_scene_content_spatially(self, pdf, original_content: str, scene_heading: str) -> str:
        """
        Enhance scene content using spatial analysis to fix action/dialogue spacing
        """
        if not original_content:
            return original_content

        try:
            # Find the scene in the PDF using the heading
            scene_page, scene_start_y = self._find_scene_in_pdf(pdf, scene_heading)
            if scene_page is None:
                logger.warning(f"Could not locate scene '{scene_heading[:30]}...' in PDF")
                return original_content

            # Extract spatial elements for this scene
            spatial_elements = self._extract_scene_spatial_elements(scene_page, scene_start_y)

            # Rebuild content with proper spacing
            enhanced_content = self._rebuild_content_with_spacing(spatial_elements, original_content)

            return enhanced_content

        except Exception as e:
            logger.error(f"Error enhancing scene content: {e}")
            return original_content

    def _find_scene_in_pdf(self, pdf, scene_heading: str) -> Tuple[Any, float]:
        """
        Find the page and Y-coordinate where a scene heading appears
        """
        clean_heading = scene_heading.strip().upper()

        for page in pdf.pages:
            try:
                # Extract text with layout preservation
                text = page.extract_text(layout=True)
                if not text:
                    continue

                lines = text.split('\n')
                for i, line in enumerate(lines):
                    if clean_heading in line.strip().upper():
                        # Estimate Y coordinate (rough approximation)
                        page_height = page.height
                        y_position = page_height * (i / len(lines))
                        return page, y_position

            except Exception as e:
                logger.warning(f"Error searching page: {e}")
                continue

        return None, 0

    def _extract_scene_spatial_elements(self, page, start_y: float) -> List[Dict[str, Any]]:
        """
        Extract spatial elements for a specific scene section
        """
        elements = []

        try:
            # Extract words with spatial positioning
            words = page.extract_words(
                x_tolerance=self.SPATIAL_CONFIG['x_tolerance'],
                y_tolerance=self.SPATIAL_CONFIG['y_tolerance']
            )

            # Filter words that are in our scene area (rough approximation)
            scene_words = [w for w in words if w['top'] >= start_y - 50]  # 50pt buffer

            # Group words into lines
            lines_dict = {}
            for word in scene_words:
                y_coord = round(word['top'])
                if y_coord not in lines_dict:
                    lines_dict[y_coord] = []
                lines_dict[y_coord].append(word)

            # Create line elements
            for y_coord in sorted(lines_dict.keys()):
                line_words = sorted(lines_dict[y_coord], key=lambda w: w['x0'])
                line_text = ' '.join(word['text'] for word in line_words)

                if line_text.strip():
                    left_margin = min(word['x0'] for word in line_words)

                    elements.append({
                        'text': line_text.strip(),
                        'y': y_coord,
                        'x': left_margin,
                        'indent': left_margin,
                        'type': self._classify_line_spatially(line_text.strip(), left_margin)
                    })

        except Exception as e:
            logger.error(f"Error extracting spatial elements: {e}")

        return elements

    def _classify_line_spatially(self, text: str, indent: float) -> str:
        """
        Classify line type based on spatial positioning
        """
        # Scene headings (left margin, specific patterns)
        if indent < 20 and re.match(r'^(INT\.|EXT\.|EST\.|I/E\.)', text.upper()):
            return 'scene_heading'

        # Character names (centered, all caps)
        if 35 <= indent <= 50 and text == text.upper() and len(text) < 40:
            # Exclude camera directions
            if not re.search(r'(CLOSE|WIDE|ANGLE|SHOT|CUT)', text.upper()):
                return 'character'

        # Parentheticals
        if text.startswith('(') and text.endswith(')'):
            return 'parenthetical'

        # Dialogue (indented, mixed case)
        if 20 <= indent <= 40 and text != text.upper():
            return 'dialogue'

        # Default to action
        return 'action'

    def _rebuild_content_with_spacing(self, spatial_elements: List[Dict], original_content: str) -> str:
        """
        Rebuild content with proper spacing based on spatial analysis
        """
        if not spatial_elements:
            return original_content

        lines = []
        previous_type = None

        for element in spatial_elements:
            element_type = element['type']
            text = element['text']

            # Add spacing based on transitions
            if self._needs_spacing_before(element_type, previous_type):
                lines.append('')  # Add blank line

            lines.append(text)

            # Add spacing after certain elements
            if self._needs_spacing_after(element_type):
                lines.append('')  # Add blank line

            previous_type = element_type

        enhanced_content = '\n'.join(lines)

        # Clean up excessive blank lines
        enhanced_content = re.sub(r'\n\n\n+', '\n\n', enhanced_content)

        return enhanced_content.strip()

    def _needs_spacing_before(self, current_type: str, previous_type: str) -> bool:
        """
        Determine if spacing is needed before current element
        """
        if not previous_type:
            return False

        # Add space before character names after action
        if current_type == 'character' and previous_type == 'action':
            return True

        # Add space before action after dialogue blocks
        if current_type == 'action' and previous_type in ['dialogue', 'parenthetical']:
            return True

        return False

    def _needs_spacing_after(self, element_type: str) -> bool:
        """
        Determine if spacing is needed after current element
        """
        # Add space after scene headings
        if element_type == 'scene_heading':
            return True

        return False

# Integration function
def enhance_with_spatial_analysis(pdf_path: str, standard_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enhance standard parser result with spatial analysis
    """
    parser = SimplifiedSpatialParser()
    return parser.enhance_standard_parser_output(pdf_path, standard_result)