"""
Enhanced Title Page and Screenplay Start Detection Utility

This module provides comprehensive detection of:
1. Title pages to skip
2. Page number detection (PAGE 1, 1., etc.)
3. Screenplay opening patterns (FADE IN, OVER BLACK, etc.)
4. Scene heading detection (INT., EXT., etc.)

Designed to work with pdfplumber text extraction and improve parsing accuracy.
"""

import re
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class TitlePageDetector:
    """Enhanced title page detection and screenplay start identification"""

    def __init__(self):
        self.screenplay_start_patterns = self._build_screenplay_start_patterns()
        self.title_page_patterns = self._build_title_page_patterns()
        self.page_number_patterns = self._build_page_number_patterns()

    def _build_screenplay_start_patterns(self) -> List[str]:
        """Build comprehensive patterns for screenplay openings"""
        return [
            # Opening transitions and scene starters
            r'^FADE\s+IN:?.*',                    # FADE IN, FADE IN:
            r'^FADE\s+IN\s+--.*',                # FADE IN --
            r'^FADE\s+IN\s+TO:?.*',              # FADE IN TO:
            r'^FADE\s+UP.*',                     # FADE UP
            r'^OVER\s+BLACK.*',                  # OVER BLACK, OVER BLACK --
            r'^BLACK\s+SCREEN.*',                # BLACK SCREEN
            r'^PRE\s*-?\s*LAP:?.*',             # PRE LAP, PRE-LAP, PRELAP:
            r'^COLD\s+OPEN.*',                   # COLD OPEN
            r'^TEASER.*',                        # TEASER

            # Scene headings (INT/EXT variations)
            r'^INT\.?\s+.*',                     # INT. BEDROOM - DAY
            r'^EXT\.?\s+.*',                     # EXT. HOUSE - NIGHT
            r'^INT\s*/\s*EXT\.?\s+.*',          # INT/EXT. CAR - DAY
            r'^I/E\.?\s+.*',                     # I/E. OFFICE - DAY
            r'^INTERIOR\.?\s+.*',                # INTERIOR. HOUSE
            r'^EXTERIOR\.?\s+.*',                # EXTERIOR. PARK

            # Time-specific scene openings
            r'^CONTINUOUS.*',                    # CONTINUOUS
            r'^LATER.*',                         # LATER
            r'^MOMENTS\s+LATER.*',               # MOMENTS LATER
            r'^THE\s+NEXT\s+DAY.*',             # THE NEXT DAY
            r'^NIGHT.*',                         # NIGHT (when used as scene start)
            r'^DAY.*',                           # DAY (when used as scene start)
            r'^MORNING.*',                       # MORNING
            r'^EVENING.*',                       # EVENING

            # Special opening elements
            r'^TITLE\s+CARD:?.*',               # TITLE CARD:
            r'^SUPER:?.*',                       # SUPER:
            r'^SUPER\s+TITLE:?.*',              # SUPER TITLE:
            r'^INSERT.*',                        # INSERT
            r'^CLOSE\s+UP.*',                   # CLOSE UP
            r'^CLOSE-UP.*',                     # CLOSE-UP

            # Voice over and narration starts
            r'^NARRATOR.*',                      # NARRATOR
            r'^V\.?O\.?.*',                     # V.O., VO
            r'^VOICE\s*-?\s*OVER.*',            # VOICE-OVER, VOICE OVER

            # Montage and sequence starts
            r'^BEGIN\s+MONTAGE.*',              # BEGIN MONTAGE
            r'^START\s+MONTAGE.*',              # START MONTAGE
            r'^MONTAGE:?.*',                    # MONTAGE:
            r'^SERIES\s+OF\s+SHOTS:?.*',       # SERIES OF SHOTS:
            r'^SEQUENCE:?.*',                   # SEQUENCE:

            # Commercial script patterns
            r'^OPEN\s+ON:?.*',                  # OPEN ON:
            r'^WE\s+OPEN\s+ON.*',              # WE OPEN ON
            r'^WE\s+SEE.*',                     # WE SEE
            r'^STOCK\s+FOOTAGE.*',              # STOCK FOOTAGE
        ]

    def _build_title_page_patterns(self) -> List[str]:
        """Build patterns that indicate title page content"""
        return [
            # Contact information
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
            r'\(\d{3}\)\s*\d{3}-\d{4}',                               # Phone (XXX) XXX-XXXX
            r'\d{3}-\d{3}-\d{4}',                                     # Phone XXX-XXX-XXXX
            r'\b\d{1,5}\s+[A-Z][a-z]+\s+(Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd)\b',  # Address

            # Dates and versions
            r'\b\d{1,2}[/.]\d{1,2}[/.]\d{2,4}\b',                   # Date formats
            r'(?i)(first|second|third|final|revised?)\s+(draft|version)',  # Draft versions
            r'(?i)draft\s+#?\d+',                                     # Draft #1
            r'(?i)version\s+\d+(\.\d+)?',                            # Version 1.0
            r'(?i)revision\s+\d+',                                    # Revision 1

            # Copyright and legal
            r'(?i)copyright|©|\(c\)\s*\d{4}',                       # Copyright
            r'(?i)all\s+rights\s+reserved',                         # All rights reserved
            r'(?i)property\s+of',                                    # Property of
            r'(?i)confidential',                                     # Confidential

            # Title page specific text
            r'(?i)written\s+by',                                     # Written by
            r'(?i)screenplay\s+by',                                  # Screenplay by
            r'(?i)story\s+by',                                       # Story by
            r'(?i)created\s+by',                                     # Created by
            r'(?i)adapted\s+from',                                   # Adapted from
            r'(?i)based\s+on',                                       # Based on

            # Episode/Show information
            r'(?i)episode\s+\d+',                                    # Episode 1
            r'(?i)season\s+\d+',                                     # Season 1
            r'"[^"]*"',                                              # Quoted titles

            # Production information
            r'(?i)production\s+(company|studio)',                    # Production company
            r'(?i)(executive\s+)?producer',                          # Producer
            r'(?i)director',                                         # Director

            # Character lists and cast
            r'(?i)characters?:?$',                                   # CHARACTERS:
            r'(?i)cast\s+(of\s+characters?)?:?$',                   # CAST OF CHARACTERS:
            r'(?i)dramatis\s+personae',                             # DRAMATIS PERSONAE

            # Agent/Representative info
            r'(?i)represented\s+by',                                # Represented by
            r'(?i)agent:?',                                         # Agent:
            r'(?i)manager:?',                                       # Manager:
            r'(?i)entertainment',                                   # Entertainment (agency names)

            # WGA registration
            r'(?i)wga\s+(registration|reg)',                        # WGA Registration
            r'(?i)registered\s+with',                               # Registered with
        ]

    def _build_page_number_patterns(self) -> List[str]:
        """Build patterns for detecting page numbers, especially PAGE 1"""
        return [
            r'^\s*PAGE\s+1\s*$',                 # PAGE 1
            r'^\s*1\.\s*$',                      # 1.
            r'^\s*-\s*1\s*-\s*$',               # - 1 -
            r'^\s*\[\s*1\s*\]\s*$',             # [1]
            r'^\s*\(\s*1\s*\)\s*$',             # (1)
            r'^\s*1\s*/\s*\d+\s*$',             # 1/120
            r'^\s*Page\s+1\s+of\s+\d+\s*$',     # Page 1 of 120
            r'^\s*1\s*$',                        # Just "1" alone on a line
        ]

    def detect_title_pages(self, pages_data: List[Dict]) -> Tuple[int, str]:
        """
        Detect which pages are title pages and find the actual screenplay start.

        Returns:
            Tuple of (start_page_index, detection_reason)
            start_page_index: 0-based index of first screenplay page
            detection_reason: Description of why this page was chosen
        """
        logger.info(f"🔍 Analyzing {len(pages_data)} pages for title page detection...")

        # Strategy 1: Look for explicit PAGE 1 markers
        page_1_detection = self._detect_explicit_page_1(pages_data)
        if page_1_detection[0] is not None:
            logger.info(f"✅ Found explicit PAGE 1 marker: {page_1_detection[1]}")
            return page_1_detection

        # Strategy 2: Look for screenplay opening patterns
        screenplay_start = self._detect_screenplay_opening(pages_data)
        if screenplay_start[0] is not None:
            logger.info(f"✅ Found screenplay opening pattern: {screenplay_start[1]}")
            return screenplay_start

        # Strategy 3: Analyze title page content density
        content_analysis = self._analyze_title_page_content(pages_data)
        if content_analysis[0] is not None:
            logger.info(f"✅ Title page detected by content analysis: {content_analysis[1]}")
            return content_analysis

        # Strategy 4: Default fallback - skip first page if it looks like title page
        if len(pages_data) > 1:
            first_page_text = pages_data[0].get('text', '').strip()
            if self._is_likely_title_page(first_page_text):
                logger.info("⚠️ Using fallback: First page appears to be title page")
                return (1, "Fallback: First page appears to be title page based on content patterns")

        # No title page detected
        logger.info("📄 No title page detected, starting from page 1")
        return (0, "No title page detected, starting from beginning")

    def _detect_explicit_page_1(self, pages_data: List[Dict]) -> Tuple[Optional[int], str]:
        """Look for explicit PAGE 1 markers"""
        for i, page_data in enumerate(pages_data):
            text = page_data.get('text', '')
            lines = text.split('\n')

            for line in lines:
                line_stripped = line.strip()
                for pattern in self.page_number_patterns:
                    if re.match(pattern, line_stripped, re.IGNORECASE):
                        logger.info(f"🎯 Found PAGE 1 marker on page {i+1}: '{line_stripped}'")
                        return (i, f"Explicit PAGE 1 marker found: '{line_stripped}'")

        return (None, "No explicit PAGE 1 marker found")

    def _detect_screenplay_opening(self, pages_data: List[Dict]) -> Tuple[Optional[int], str]:
        """Look for screenplay opening patterns like FADE IN, OVER BLACK, etc."""
        for i, page_data in enumerate(pages_data):
            text = page_data.get('text', '')
            lines = text.split('\n')

            # Look in first 20 lines of each page for screenplay openings
            for line_idx, line in enumerate(lines[:20]):
                line_stripped = line.strip().upper()
                if not line_stripped:
                    continue

                for pattern in self.screenplay_start_patterns:
                    if re.match(pattern, line_stripped):
                        logger.info(f"🎬 Found screenplay opening on page {i+1}, line {line_idx+1}: '{line_stripped}'")
                        return (i, f"Screenplay opening pattern found: '{line_stripped}'")

        return (None, "No screenplay opening patterns found")

    def _analyze_title_page_content(self, pages_data: List[Dict]) -> Tuple[Optional[int], str]:
        """Analyze content density and patterns to identify title pages"""
        title_page_scores = []

        for i, page_data in enumerate(pages_data):
            text = page_data.get('text', '')
            score = self._calculate_title_page_score(text)
            title_page_scores.append(score)
            logger.debug(f"Page {i+1} title page score: {score:.2f}")

        # Find the first page with a low title page score (likely screenplay content)
        threshold = 0.3  # Adjust based on testing
        for i, score in enumerate(title_page_scores):
            if score < threshold:
                if i > 0:  # There was at least one title page before this
                    reason = f"Content analysis: Pages 1-{i} appear to be title pages (scores: {[f'{s:.2f}' for s in title_page_scores[:i+1]]}, threshold: {threshold})"
                    return (i, reason)
                break

        return (None, "Content analysis inconclusive")

    def _calculate_title_page_score(self, text: str) -> float:
        """Calculate how likely text is to be from a title page (0.0 = screenplay, 1.0 = title page)"""
        if not text.strip():
            return 0.0

        score = 0.0
        total_patterns = len(self.title_page_patterns)

        # Check for title page patterns
        matches = 0
        for pattern in self.title_page_patterns:
            if re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
                matches += 1

        pattern_score = matches / total_patterns if total_patterns > 0 else 0.0
        score += pattern_score * 0.6  # 60% weight for pattern matching

        # Check for screenplay content (negative indicators for title page)
        screenplay_indicators = 0
        for pattern in self.screenplay_start_patterns:
            if re.search(pattern, text.upper()):
                screenplay_indicators += 1

        screenplay_score = min(screenplay_indicators / 10.0, 1.0)  # Normalize
        score -= screenplay_score * 0.4  # Subtract screenplay indicators

        # Text density and formatting analysis
        lines = text.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]

        if len(non_empty_lines) > 0:
            # Title pages often have centered, short lines
            avg_line_length = sum(len(line.strip()) for line in non_empty_lines) / len(non_empty_lines)
            if avg_line_length < 40:  # Short lines suggest title page
                score += 0.2

            # Check for typical title page structure (few long lines, lots of whitespace)
            if len(non_empty_lines) < len(lines) / 2:  # More than 50% empty lines
                score += 0.2

        return max(0.0, min(1.0, score))  # Clamp between 0 and 1

    def _is_likely_title_page(self, text: str) -> bool:
        """Quick check if text looks like a title page"""
        return self._calculate_title_page_score(text) > 0.5

    def generate_screenplay_opening_regex(self) -> str:
        """Generate a single regex pattern for all screenplay openings"""
        return '|'.join(f'({pattern})' for pattern in self.screenplay_start_patterns)

    def get_screenplay_opening_examples(self) -> List[str]:
        """Get examples of valid screenplay openings for documentation"""
        return [
            "FADE IN:",
            "FADE IN --",
            "OVER BLACK",
            "INT. BEDROOM - DAY",
            "EXT. HOUSE - NIGHT",
            "INT/EXT. CAR - DAY",
            "I/E. OFFICE - CONTINUOUS",
            "COLD OPEN",
            "TEASER",
            "PRE LAP:",
            "TITLE CARD: \"One Year Later\"",
            "SUPER: \"New York City\"",
            "NARRATOR (V.O.)",
            "BEGIN MONTAGE",
            "SERIES OF SHOTS:",
            "WE OPEN ON:",
        ]