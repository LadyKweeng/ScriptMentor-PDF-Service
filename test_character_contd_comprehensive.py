#!/usr/bin/env python3
"""
Comprehensive CHARACTER (CONT'D) Pattern Test Suite
===================================================

Tests all possible CHARACTER (CONT'D) pattern variations and edge cases
to validate proper character and dialogue classification.
"""

import sys
import re
from screenplay_parser import ElementClassifier

def test_character_contd_patterns():
    """Test all CHARACTER (CONT'D) pattern variations"""
    print("🧪 COMPREHENSIVE CHARACTER (CONT'D) PATTERN TEST SUITE")
    print("=" * 70)

    # Test cases covering all possible corrupted patterns
    test_cases = [
        # Standard patterns
        ("HANNAH (CONT'D)", "Standard CONT'D pattern"),
        ("HANNAH (MORE)", "Standard MORE pattern"),

        # Corrupted patterns from PDF extraction
        ("HANNAH (CCOONNTT'DD)", "Double letters with mixed quotes"),
        ("HANNAH (CCOONNTT''DD)", "Double letters with double quotes"),
        ("HANNAH (CCOONNTTDD)", "Double letters no quotes"),
        ("HANNAH (CCCOOONNNTTT'DD)", "Triple letters"),
        ("HANNAH (CCCOOONNNTTT''DD)", "Triple letters double quotes"),

        # Spacing variations
        ("HANNAH  (CONT'D)", "Double space before parenthesis"),
        ("HANNAH   (CCOONNTT'DD)", "Triple space"),
        ("HANNAH(CONT'D)", "No space before parenthesis"),

        # Case variations (should still work)
        ("HANNAH (CONT'd)", "Lowercase d"),
        ("HANNAH (Cont'D)", "Mixed case"),

        # Character name variations
        ("SARAH CHEN (CONT'D)", "Full name with space"),
        ("DR. WILLIAMS (CCOONNTT'DD)", "Title with period"),
        ("VOICE-OVER (CONT'D)", "Hyphenated character"),
        ("ANNOUNCER #2 (MORE)", "Character with number"),

        # Different indentations
        ("HANNAH (CONT'D)", "Left margin (0 spaces)"),
        ("    HANNAH (CONT'D)", "4 spaces"),
        ("        HANNAH (CONT'D)", "8 spaces"),
        ("                         HANNAH (CONT'D)", "25 spaces (dialogue indent)"),
        ("                                        HANNAH (CONT'D)", "40 spaces (character indent)"),

        # Edge cases that should NOT be detected as CHARACTER (CONT'D)
        ("(CONT'D)", "Parenthetical only - should be action"),
        ("HANNAH CONTINUED SPEAKING", "Spelled out - should be action"),
        ("The story continues (CONT'D)", "Mid-sentence - should be action"),
    ]

    classifier = ElementClassifier()
    total_tests = len(test_cases)
    passed_tests = 0
    failed_tests = []

    for i, (test_pattern, description) in enumerate(test_cases, 1):
        leading_spaces = len(test_pattern) - len(test_pattern.lstrip())
        result = classifier.classify_line(test_pattern, 0, [test_pattern])

        # Expected result logic
        should_be_character = any(pattern in test_pattern.upper() for pattern in [
            "(CONT'D)", "(MORE)", "(CCOONNTT", "(CCCOOONNNTTT"
        ]) and not test_pattern.startswith("(") and "continues" not in test_pattern.lower()

        expected_type = "character" if should_be_character else "action"
        is_correct = result["type"] == expected_type

        status = "✅ PASS" if is_correct else "❌ FAIL"
        passed_tests += is_correct

        if not is_correct:
            failed_tests.append((test_pattern, description, result["type"], expected_type))

        print(f"Test {i:2d}: {status} | {result['type']:9s} | \"{test_pattern}\" ({description})")

    # Test dialogue continuation after CHARACTER (CONT'D)
    print("\n" + "=" * 70)
    print("🎭 TESTING DIALOGUE CONTINUATION AFTER CHARACTER (CONT'D)")
    print("=" * 70)

    dialogue_test_cases = [
        # Standard continuation
        [
            "                                        HANNAH (CONT'D)",
            "                         I can't believe this happened.",
            "                         What are we going to do now?"
        ],
        # Corrupted continuation at different indentations
        [
            "HANNAH (CCOONNTT'DD)",  # Left margin
            "I can make more on these jerk-offs,",
            "pump-n-dumps, than I would in the",
            "stock market."
        ],
        # Mixed indentation continuation
        [
            "                         HANNAH  (CCOONNTT''DD)",  # 25 spaces
            "                         Sort of... A 401k, pension,",
            "                         all those twentieth-century",
            "                         ideas are dead."
        ]
    ]

    dialogue_passed = 0
    dialogue_total = 0

    for case_num, dialogue_lines in enumerate(dialogue_test_cases, 1):
        print(f"\nDialogue Test Case {case_num}:")
        classifier = ElementClassifier()  # Fresh classifier for each test

        for line_num, line in enumerate(dialogue_lines):
            leading_spaces = len(line) - len(line.lstrip())
            result = classifier.classify_line(line, line_num, dialogue_lines)

            expected = "character" if line_num == 0 else "dialogue"
            is_correct = result["type"] == expected
            status = "✅" if is_correct else "❌"

            dialogue_total += 1
            dialogue_passed += is_correct

            print(f"  Line {line_num + 1}: {status} {result['type']:9s} | \"{line}\" (indent: {leading_spaces})")

    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 70)
    print(f"Character Pattern Tests: {passed_tests}/{total_tests} passed ({passed_tests/total_tests*100:.1f}%)")
    print(f"Dialogue Continuation Tests: {dialogue_passed}/{dialogue_total} passed ({dialogue_passed/dialogue_total*100:.1f}%)")

    overall_passed = passed_tests + dialogue_passed
    overall_total = total_tests + dialogue_total
    print(f"Overall: {overall_passed}/{overall_total} passed ({overall_passed/overall_total*100:.1f}%)")

    if failed_tests:
        print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
        for pattern, desc, actual, expected in failed_tests:
            print(f"  • \"{pattern}\" - Expected: {expected}, Got: {actual} ({desc})")

    if overall_passed == overall_total:
        print("\n🎉 ALL TESTS PASSED! CHARACTER (CONT'D) parsing is working correctly.")
        return True
    else:
        print(f"\n⚠️  {overall_total - overall_passed} tests failed. Fix needed.")
        return False

def test_regex_patterns_directly():
    """Test regex patterns directly to debug pattern matching"""
    print("\n" + "=" * 70)
    print("🔍 DIRECT REGEX PATTERN TESTING")
    print("=" * 70)

    # Current patterns from our code
    patterns = [
        r'\b[A-Z][A-Z\s\-]+\s*\((CONT\'D|CCOONNTT[\'\']*DD|MORE)\)',  # ElementClassifier
        r'\b[A-Z][A-Z\s\-]+\s*\((CONT\'D|CCOONNTT[\'\']*DD|MORE)\)'   # EnhancedScreenplayPatterns
    ]

    test_strings = [
        "HANNAH (CONT'D)",
        "HANNAH (CCOONNTT'DD)",
        "HANNAH (CCOONNTT''DD)",
        "HANNAH  (CCOONNTT''DD)",  # Double space
        "SARAH CHEN (MORE)",
        "(CONT'D)",  # Should not match
        "The story continues"  # Should not match
    ]

    for i, pattern in enumerate(patterns, 1):
        print(f"\nPattern {i}: {pattern}")
        for test_string in test_strings:
            match = re.search(pattern, test_string)
            status = "✅ MATCH" if match else "❌ NO MATCH"
            print(f"  {status} | \"{test_string}\"")

if __name__ == "__main__":
    print("Starting comprehensive CHARACTER (CONT'D) testing...\n")

    success = test_character_contd_patterns()
    test_regex_patterns_directly()

    print(f"\n{'🎉 SUCCESS' if success else '❌ FAILURES DETECTED'}: CHARACTER (CONT'D) testing complete.")
    sys.exit(0 if success else 1)