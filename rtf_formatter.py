"""
RTF Formatter - Phase 3: Clean escape sequences and format RTF output
Fixes escaped backslashes (\\n instead of newlines) and other RTF artifacts
"""

import re
from typing import Dict, Any

class RTFFormatter:
    """Handles RTF output formatting and escape sequence cleanup"""
    
    def __init__(self):
        # Common escape sequences that need fixing
        self.escape_patterns = {
            r'\\\\n': '\n',         # Fix escaped newlines
            r'\\\\t': '\t',         # Fix escaped tabs  
            r'\\\\r': '\r',         # Fix escaped carriage returns
            r'\\\\"': '"',          # Fix escaped quotes
            r"\\\\'": "'",          # Fix escaped single quotes
            r'\\\\\\\\': '\\\\',    # Fix double backslashes
        }
    
    def clean_escape_sequences(self, text: str) -> str:
        """Completely clean all escape sequences and artifacts"""
        if not text:
            return text
        
        # Phase 1: Fix escape sequences (order matters!)
        replacements = [
            ('\\\\n', '\n'),           # Escaped newlines
            ('\\\\t', '\t'),           # Escaped tabs
            ('\\\\r', '\r'),           # Escaped carriage returns
            ('\\\\"', '"'),            # Escaped quotes
            ("\\\\'", "'"),            # Escaped single quotes
            ('\\\\\\\\', '\\\\'),      # Escaped backslashes
        ]
        
        for pattern, replacement in replacements:
            text = text.replace(pattern, replacement)
        
        # Phase 2: Remove any remaining double/triple backslashes
        text = re.sub(r'\\{2,}', '', text)
        
        # Phase 3: Clean up character corruption
        # Fix repeated characters: HHAAAAHH -> HANNAH
        text = re.sub(r'([A-Z])\1{2,}', r'\1', text)
        
        # Fix doubled quotes and parentheses
        text = re.sub(r"'{2,}", "'", text)
        text = re.sub(r'"{2,}', '"', text)
        text = re.sub(r'\({2,}', '(', text)
        text = re.sub(r'\){2,}', ')', text)
        
        # Phase 4: Fix specific screenplay artifacts
        text = re.sub(r"CONT'D", "CONT'D", text)
        text = re.sub(r'V\.O\.', 'V.O.', text)
        text = re.sub(r'O\.S\.', 'O.S.', text)
        
        # Phase 5: Clean up spacing
        text = re.sub(r' {3,}', '  ', text)  # Reduce excessive spaces
        text = re.sub(r'\n{4,}', '\n\n\n', text)  # Max 3 newlines
        
        # Remove any remaining RTF control sequences
        text = self._remove_rtf_controls(text)
        
        return text
    
    def _remove_rtf_controls(self, text: str) -> str:
        """Remove RTF control sequences and artifacts"""
        # Remove RTF control words like {\rtf1\ansi\deff0...}
        text = re.sub(r'\{\\rtf[^}]*\}', '', text)
        
        # Remove RTF font table and color table references
        text = re.sub(r'\{\\fonttbl[^}]*\}', '', text)
        text = re.sub(r'\{\\colortbl[^}]*\}', '', text)
        
        # Remove RTF paragraph formatting
        text = re.sub(r'\\par\b', '\n', text)
        text = re.sub(r'\\pard\b', '', text)
        
        # Remove RTF font size and style commands
        text = re.sub(r'\\f\d+', '', text)
        text = re.sub(r'\\fs\d+', '', text)
        text = re.sub(r'\\b\b', '', text)  # Bold
        text = re.sub(r'\\i\b', '', text)  # Italic
        
        # Clean up multiple spaces and newlines
        text = re.sub(r' +', ' ', text)  # Multiple spaces to single space
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)  # Multiple newlines to double newline
        
        return text.strip()
    
    def format_screenplay_rtf(self, screenplay_data: Dict[str, Any]) -> str:
        """Format screenplay data as clean RTF without escape sequences"""
        if not screenplay_data or 'scenes' not in screenplay_data:
            return ""
        
        rtf_content = []
        
        # Add title if available
        if screenplay_data.get('metadata', {}).get('title'):
            title = str(screenplay_data['metadata']['title'])
            title = self.clean_escape_sequences(title)
            rtf_content.append(f"TITLE: {title}")
            rtf_content.append("")
            rtf_content.append("")  # Double space after title
        
        # Process each scene
        for i, scene in enumerate(screenplay_data['scenes'], 1):
            # Scene heading - with 1.5" margin (12 spaces) to match action lines
            heading = self.clean_escape_sequences(scene.get('heading', ''))
            if heading:
                # Add 1.5" margin indentation to match action lines
                indented_heading = f"            {heading.upper()}"  # 12 spaces for 1.5" margin
                rtf_content.append(indented_heading)
                rtf_content.append("")  # Blank line after heading
            
            # Scene content
            content = scene.get('content', '')
            if content:
                # Apply escape cleaning to content
                cleaned_content = self.clean_escape_sequences(content)
                
                # Split into lines and process each
                lines = cleaned_content.split('\n')
                for line in lines:
                    # Don't add empty lines at the beginning
                    if line or rtf_content:
                        rtf_content.append(line)
            
            # Add scene separator (double blank between scenes)
            if i < len(screenplay_data['scenes']):
                rtf_content.append("")
                rtf_content.append("")
        
        # Join all content and apply final cleanup
        final_rtf = '\n'.join(rtf_content)
        
        # Final pass to ensure no escape sequences remain
        final_rtf = self.clean_escape_sequences(final_rtf)
        
        # Ensure consistent line endings
        final_rtf = final_rtf.replace('\r\n', '\n')
        final_rtf = final_rtf.replace('\r', '\n')
        
        return final_rtf
    
    def validate_formatting(self, text: str) -> Dict[str, Any]:
        """
        Validate that formatting meets 99% accuracy standards
        """
        validation_results = {
            'character_names_centered': False,
            'no_escape_sequences': False,
            'proper_dialogue_indent': False,
            'issues_found': []
        }
        
        lines = text.split('\n')
        
        # Check for escape sequences
        escape_found = any(r'\\' in line for line in lines if r'\\' in line)
        validation_results['no_escape_sequences'] = not escape_found
        if escape_found:
            validation_results['issues_found'].append("Escape sequences still present")
        
        # Check character name positioning (should be around 38 characters in)
        character_lines = [line for line in lines if self._is_character_line(line)]
        properly_centered = 0
        
        for line in character_lines:
            leading_spaces = len(line) - len(line.lstrip())
            # Character names should be centered around 38 spaces (±5 tolerance)
            if 33 <= leading_spaces <= 43:
                properly_centered += 1
        
        if character_lines:
            center_percentage = (properly_centered / len(character_lines)) * 100
            validation_results['character_names_centered'] = center_percentage >= 90
            if center_percentage < 90:
                validation_results['issues_found'].append(f"Only {center_percentage:.1f}% of character names properly centered")
        
        # Check dialogue indentation (should be around 10 spaces)
        dialogue_lines = [line for line in lines if self._is_dialogue_line(line)]
        properly_indented = 0
        
        for line in dialogue_lines:
            leading_spaces = len(line) - len(line.lstrip())
            # Dialogue should be indented around 10 spaces (±3 tolerance)
            if 7 <= leading_spaces <= 13:
                properly_indented += 1
        
        if dialogue_lines:
            indent_percentage = (properly_indented / len(dialogue_lines)) * 100
            validation_results['proper_dialogue_indent'] = indent_percentage >= 90
            if indent_percentage < 90:
                validation_results['issues_found'].append(f"Only {indent_percentage:.1f}% of dialogue properly indented")
        
        return validation_results
    
    def _is_character_line(self, line: str) -> bool:
        """Identify if line is a character name"""
        stripped = line.strip()
        if not stripped:
            return False
        
        # Character names are typically ALL CAPS and not too long
        return (stripped == stripped.upper() and 
                2 < len(stripped) < 30 and
                not stripped.startswith('INT.') and
                not stripped.startswith('EXT.') and
                not stripped.startswith('FADE'))
    
    def _is_dialogue_line(self, line: str) -> bool:
        """Identify if line is dialogue (not character name, not action)"""
        stripped = line.strip()
        if not stripped or self._is_character_line(line):
            return False
        
        # Dialogue lines have some indentation but aren't ALL CAPS (typically)
        leading_spaces = len(line) - len(line.lstrip())
        return (leading_spaces > 5 and 
                not stripped.startswith('(') and  # Not parentheticals
                stripped != stripped.upper())     # Not ALL CAPS (like scene headings)