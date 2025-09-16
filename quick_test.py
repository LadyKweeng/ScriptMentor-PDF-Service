#!/usr/bin/env python3
"""
Quick test of current parsing functionality
"""

from screenplay_parser import ElementClassifier

def test_current_implementation():
    print("🧪 TESTING CURRENT IMPLEMENTATION")
    print("=" * 50)

    classifier = ElementClassifier()

    # Test the specific issues from Action_Spacing_Error.md
    test_lines = [
        "                         (MMOORREE)",          # Should be continuation_marker
        "                         HANNAH  (CCOONNTT''DD)",  # Should be character -> HANNAH
        "                         I can make more on these jerk-offs,",  # Should be dialogue
        "                         pump-n-dumps, than I would in the",     # Should be dialogue
        "                         stock market."                           # Should be dialogue
    ]

    print("Testing the exact scenario from Action_Spacing_Error.md:")
    print("-" * 50)

    for i, line in enumerate(test_lines):
        result = classifier.classify_line(line, i, test_lines)
        line_num = 565 + i

        print(f"Line {line_num}: \"{line.strip()}\"")
        print(f"  -> {result.get('type')}: \"{result.get('text')}\" (indent: {result.get('indent')})")
        print()

    # Test artifact cleaning directly
    print("Testing artifact cleaning:")
    print("-" * 30)

    test_artifacts = [
        "HANNAH (MMOORREE)",
        "HANNAH (CCOONNTT'DD)",
        "HANNAH (CCOONNTT''DD)",
    ]

    for artifact in test_artifacts:
        cleaned = classifier._clean_extraction_artifacts(artifact)
        print(f"Original: \"{artifact}\"")
        print(f"Cleaned:  \"{cleaned}\"")
        print()

if __name__ == "__main__":
    test_current_implementation()