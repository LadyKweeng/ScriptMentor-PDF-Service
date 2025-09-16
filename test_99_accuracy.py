#!/usr/bin/env python3
"""
Comprehensive 99% Accuracy Test Suite for Enhanced Screenplay Parser
==================================================================

Tests all the critical fixes implemented for 99% accuracy:
1. Title page detection and exclusion
2. PDF artifact cleaning (doubled characters)
3. CHARACTER (CONT'D) pattern recognition
4. Dialogue after CHARACTER (CONT'D) classification
5. Proper screenplay indentation standards
"""

import sys
import re
from screenplay_parser import ElementClassifier

def test_title_page_exclusion():
    """Test that title page content is properly excluded"""
    print("🧪 TESTING TITLE PAGE EXCLUSION")
    print("=" * 50)

    classifier = ElementClassifier()

    title_page_lines = [
        "Written By Darwin Serink",
        "darwinserink@gmail.com",
        "02.27.25",
        "EPISODE 101",
        '"COLD STORAGE"',
        "WAGMI",
        "[Wag-Me] {Acronym}",
        "Related to \"NGMI\"(not going to make it)",
        "Anon 1: Holy shit, Bitcoin is mooning!"
    ]

    all_lines = title_page_lines + ["OVER BLACK --", "Scene content starts here"]

    passed = 0
    total = len(title_page_lines)

    for i, line in enumerate(title_page_lines):
        result = classifier.classify_line(line, i, all_lines)

        if result.get('type') == 'title_page' and result.get('skip'):
            print(f"✅ SKIP: \"{line}\"")
            passed += 1
        else:
            print(f"❌ FAIL: \"{line}\" -> {result.get('type')}")

    print(f"Title Page Exclusion: {passed}/{total} ({passed/total*100:.1f}%)")
    return passed == total

def test_pdf_artifact_cleaning():
    """Test PDF artifact cleaning functionality"""
    print("\\n🧪 TESTING PDF ARTIFACT CLEANING")
    print("=" * 50)

    classifier = ElementClassifier()

    test_cases = [
        # Input with artifacts -> Expected clean output
        ("HANNAH (MMOORREE)", "HANNAH (MORE)"),
        ("HANNAH (CCOONNTT'DD)", "HANNAH (CONT'D)"),
        ("HANNAH (CCOONNTT''DD)", "HANNAH (CONT'D)"),
        ("HANNAH (CCCOOONNNTTT'DD)", "HANNAH (CONT'D)"),
        ("Text with smart quotes â€™", "Text with smart quotes '"),
    ]

    passed = 0
    total = len(test_cases)

    for original, expected in test_cases:
        cleaned = classifier._clean_extraction_artifacts(original)

        if cleaned == expected:
            print(f"✅ CLEAN: \"{original}\" -> \"{cleaned}\"")
            passed += 1
        else:
            print(f"❌ FAIL: \"{original}\" -> \"{cleaned}\" (expected: \"{expected}\")")

    print(f"PDF Artifact Cleaning: {passed}/{total} ({passed/total*100:.1f}%)")
    return passed == total

def test_character_contd_recognition():
    """Test CHARACTER (CONT'D) pattern recognition"""
    print("\\n🧪 TESTING CHARACTER (CONT'D) RECOGNITION")
    print("=" * 50)

    classifier = ElementClassifier()

    test_cases = [
        # All should be recognized as character type
        "HANNAH (CONT'D)",
        "HANNAH (MORE)",
        "HANNAH (MMOORREE)",  # Will be cleaned first
        "HANNAH (CCOONNTT'DD)",  # Will be cleaned first
        "SARAH CHEN (CONT'D)",
        "DR. WILLIAMS (MORE)",
    ]

    passed = 0
    total = len(test_cases)

    for test_line in test_cases:
        result = classifier.classify_line(test_line, 50, [test_line])

        if result.get('type') == 'character':
            print(f"✅ CHAR: \"{test_line}\" -> {result.get('text')} (indent: {result.get('indent')})")
            passed += 1
        else:
            print(f"❌ FAIL: \"{test_line}\" -> {result.get('type')}")

    print(f"CHARACTER (CONT'D) Recognition: {passed}/{total} ({passed/total*100:.1f}%)")
    return passed == total

def test_dialogue_after_contd():
    """Test dialogue classification after CHARACTER (CONT'D)"""
    print("\\n🧪 TESTING DIALOGUE AFTER CHARACTER (CONT'D)")
    print("=" * 50)

    # Simulate the exact scenario from Action_Spacing_Error.md
    test_scenario = [
        "                         (MMOORREE)",          # Line 565
        "                         HANNAH  (CCOONNTT''DD)",  # Line 566
        "                         I can make more on these jerk-offs,",  # Line 567 - should be DIALOGUE
        "                         pump-n-dumps, than I would in the",     # Line 568 - should be DIALOGUE
        "                         stock market."                           # Line 569 - should be DIALOGUE
    ]

    classifier = ElementClassifier()
    passed = 0
    total = 3  # Testing the 3 dialogue lines

    # Process the full sequence
    for i, line in enumerate(test_scenario):
        result = classifier.classify_line(line, i, test_scenario)
        line_num = 565 + i

        if i == 0:  # (MORE) marker
            expected = 'continuation_marker'
        elif i == 1:  # CHARACTER (CONT'D)
            expected = 'character'
        else:  # Should be dialogue
            expected = 'dialogue'
            if result.get('type') == 'dialogue':
                print(f"✅ DIALOGUE: Line {line_num}: \"{line.strip()}\" (indent: {result.get('indent')})")
                passed += 1
            else:
                print(f"❌ FAIL: Line {line_num}: \"{line.strip()}\" -> {result.get('type')} (expected: dialogue)")

        if i <= 1:  # Don't count MORE and CHARACTER in dialogue stats
            if result.get('type') == expected:
                print(f"✅ {expected.upper()}: Line {line_num}: \"{line.strip()}\"")

    print(f"Dialogue After CONT'D: {passed}/{total} ({passed/total*100:.1f}%)")
    return passed == total

def test_indentation_standards():
    """Test proper screenplay indentation"""
    print("\\n🧪 TESTING INDENTATION STANDARDS")
    print("=" * 50)

    classifier = ElementClassifier()

    # Test proper indentation values
    expected_indents = {
        'character': 38,
        'dialogue': 25,
        'action': 12,
        'scene_heading': 12,
        'parenthetical': 30,
        'transition': 55,
    }

    passed = 0
    total = len(expected_indents)

    for element_type, expected_indent in expected_indents.items():
        actual_indent = classifier._calculate_proper_indent(element_type)

        if actual_indent == expected_indent:
            print(f"✅ INDENT: {element_type} -> {actual_indent} spaces")
            passed += 1
        else:
            print(f"❌ FAIL: {element_type} -> {actual_indent} (expected: {expected_indent})")

    print(f"Indentation Standards: {passed}/{total} ({passed/total*100:.1f}%)")
    return passed == total

def test_action_vs_dialogue_classification():
    """Test proper action vs dialogue classification"""
    print("\\n🧪 TESTING ACTION VS DIALOGUE CLASSIFICATION")
    print("=" * 50)

    classifier = ElementClassifier()

    test_cases = [
        # (text, expected_type, description)
        ("Hannah shoots a disingenuous smile", "action", "Clear action description"),
        ("Roger hands the joint to Hannah.", "action", "Action with period"),
        ("You good?", "dialogue", "Clear dialogue question"),
        ("I'm chill. Appreciate the offer.", "dialogue", "Dialogue with multiple sentences"),
        ("ROGER swigs off the bottle of bubbly.", "action", "Action with character name"),
    ]

    passed = 0
    total = len(test_cases)

    # Set up dialogue context for dialogue test cases
    for text, expected_type, description in test_cases:
        if expected_type == "dialogue":
            classifier.in_dialogue_block = True
            classifier.last_element = 'character'
        else:
            classifier.in_dialogue_block = False
            classifier.last_element = None

        result = classifier.classify_line(text, 50, [text])

        if result.get('type') == expected_type:
            print(f"✅ {expected_type.upper()}: \"{text}\" - {description}")
            passed += 1
        else:
            print(f"❌ FAIL: \"{text}\" -> {result.get('type')} (expected: {expected_type})")

    print(f"Action vs Dialogue: {passed}/{total} ({passed/total*100:.1f}%)")
    return passed == total

def run_comprehensive_accuracy_test():
    """Run all tests and calculate overall accuracy"""
    print("🎯 COMPREHENSIVE 99% ACCURACY TEST SUITE")
    print("=" * 70)

    test_results = {
        "Title Page Exclusion": test_title_page_exclusion(),
        "PDF Artifact Cleaning": test_pdf_artifact_cleaning(),
        "CHARACTER (CONT'D) Recognition": test_character_contd_recognition(),
        "Dialogue After CONT'D": test_dialogue_after_contd(),
        "Indentation Standards": test_indentation_standards(),
        "Action vs Dialogue": test_action_vs_dialogue_classification(),
    }

    print("\\n" + "=" * 70)
    print("📊 FINAL ACCURACY RESULTS")
    print("=" * 70)

    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    overall_accuracy = (passed_tests / total_tests) * 100

    for test_name, passed in test_results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")

    print("=" * 70)
    print(f"📈 OVERALL ACCURACY: {passed_tests}/{total_tests} ({overall_accuracy:.1f}%)")

    if overall_accuracy >= 99.0:
        print("🎉 SUCCESS: 99%+ accuracy achieved!")
        print("✅ All critical parsing issues have been resolved")
        return True
    else:
        print(f"⚠️  NEEDS IMPROVEMENT: {100 - overall_accuracy:.1f}% accuracy gap remains")
        failed_tests = [name for name, passed in test_results.items() if not passed]
        print(f"❌ Failed tests: {', '.join(failed_tests)}")
        return False

if __name__ == "__main__":
    print("Starting 99% accuracy validation...\\n")

    success = run_comprehensive_accuracy_test()

    print(f"\\n{'🎉 SUCCESS' if success else '❌ FAILURES DETECTED'}: 99% accuracy testing complete.")
    sys.exit(0 if success else 1)