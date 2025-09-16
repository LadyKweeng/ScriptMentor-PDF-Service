#!/usr/bin/env python3
"""
Test script for verifying dialogue/action classification fixes
"""

from screenplay_parser import ScreenplayParser, ElementClassifier

def test_dialogue_continuation():
    """Test that dialogue continuations are not broken incorrectly"""
    print("=== TESTING DIALOGUE CONTINUATION ===\n")

    classifier = ElementClassifier()

    # Simulate being in a dialogue block
    classifier.in_dialogue_block = True
    classifier.last_element = 'dialogue'
    classifier.last_character = 'HANNAH (V.O.)'

    # Test problematic dialogue lines from Action_Spacing_Error.md
    test_cases = [
        # These should remain as dialogue
        ("Discord circle jerk of crypto bros", 'dialogue'),
        ("getting off on multibillion-dollar", 'dialogue'),
        ("grifts. It's like a shit casino in", 'dialogue'),
        ("Old Town Vegas with cheap vodka", 'dialogue'),
        ("drinks and penny slots, and", 'dialogue'),
        ("everyone who can count cards is", 'dialogue'),
        ("there.", 'dialogue'),

        # These should break dialogue and become action
        ("Hannah walks to the door.", 'action'),
        ("ANGLE ON: The computer screen.", 'action'),
        ("We push in on Planet Earth.", 'action'),
        ("WORK DESK", 'action'),
        ("The view of our home planet.", 'action')
    ]

    for line, expected_type in test_cases:
        result = classifier.classify_line(line, 0, [line])
        actual_type = result['type']
        status = "✅" if actual_type == expected_type else "❌"
        print(f"{status} '{line[:40]}...'")
        print(f"   Expected: {expected_type}, Got: {actual_type}")
        if actual_type != expected_type:
            print(f"   ERROR: Misclassified!")
        print()

def test_character_continuation():
    """Test character name with CONT'D detection"""
    print("=== TESTING CHARACTER (CONT'D) DETECTION ===\n")

    classifier = ElementClassifier()

    test_cases = [
        # Various CONT'D patterns
        ("HANNAH (CONT'D)", True),
        ("DE-FI DOM (CONT'D)", True),
        ("PATRICK (CONT'D)", True),
        ("HANNAH (CONT'D)", True),
        ("ROGER (CONTINUED)", True),

        # Corrupted patterns that should still work
        ("HANNAH (CON'T'D)", True),
        ("HANNAH CONT'D", True),

        # Not character names
        ("WORK DESK", False),
        ("ANGLE ON", False),
        ("FADE TO:", False)
    ]

    for text, should_be_character in test_cases:
        is_char = classifier._is_character_continuation(text)
        status = "✅" if is_char == should_be_character else "❌"
        print(f"{status} '{text}'")
        print(f"   Expected character: {should_be_character}, Got: {is_char}")
        if is_char != should_be_character:
            print(f"   ERROR: Misclassified!")
        print()

def test_page_break_dialogue():
    """Test dialogue continuing across page breaks"""
    print("=== TESTING PAGE BREAK DIALOGUE ===\n")

    parser = ScreenplayParser()

    # Simulate a page break scenario
    mock_pages = [
        {
            'page_num': 1,
            'lines': [
                '                                    HANNAH (V.O.)',
                '                         The metaverse... A pyramid scheme',
                '                         for twenty-something kleptocrats. A'
            ]
        },
        {
            'page_num': 2,
            'lines': [
                '2.',  # Page number to be filtered
                '',
                '                                    HANNAH (V.O.) (CONT\'D)',
                '                         Discord circle jerk of crypto bros',
                '                         getting off on multibillion-dollar',
                '                         grifts.'
            ]
        }
    ]

    scenes = parser._parse_sequential_content(mock_pages)

    if scenes:
        content = scenes[0].get('content', '')
        lines = content.split('\n')

        print("Parsed content:")
        for i, line in enumerate(lines[:10]):
            leading_spaces = len(line) - len(line.lstrip()) if line else 0
            print(f"Line {i}: (spaces:{leading_spaces:2d}) '{line}'")

        # Check for issues
        print("\nChecks:")
        has_page_num = any('2.' in line for line in lines)
        has_corrupted_contd = any('CCOONNTT' in line or 'CONT\'\'D' in line for line in lines)

        print(f"{'❌' if has_page_num else '✅'} Page numbers removed: {not has_page_num}")
        print(f"{'❌' if has_corrupted_contd else '✅'} CONT'D corruption fixed: {not has_corrupted_contd}")

def test_action_after_dialogue():
    """Test action immediately after dialogue"""
    print("\n=== TESTING ACTION AFTER DIALOGUE ===\n")

    parser = ScreenplayParser()

    mock_scene = [{
        'page_num': 1,
        'lines': [
            '                                    BOUNCER',
            '                         Don\'t look like it to me.',
            '',
            'Hannah rolls her smokey cat eyes. She\'s outta there.'
        ]
    }]

    scenes = parser._parse_sequential_content(mock_scene)

    if scenes:
        content = scenes[0].get('content', '')
        lines = content.split('\n')

        print("Parsed content:")
        for i, line in enumerate(lines):
            leading_spaces = len(line) - len(line.lstrip()) if line else 0
            print(f"Line {i}: (spaces:{leading_spaces:2d}) '{line}'")

        # Verify proper classification
        dialogue_indent = 25
        action_indent = 12
        character_indent = 38

        print("\nExpected formatting:")
        print(f"Line 0: Character 'BOUNCER' at {character_indent} spaces")
        print(f"Line 1: Dialogue 'Don't look...' at {dialogue_indent} spaces")
        print(f"Line 3: Action 'Hannah rolls...' at {action_indent} spaces")

def run_all_tests():
    """Run all tests"""
    test_dialogue_continuation()
    test_character_continuation()
    test_page_break_dialogue()
    test_action_after_dialogue()

    print("\n" + "="*50)
    print("TESTING COMPLETE")
    print("="*50)
    print("\nReview the results above to verify all fixes are working.")
    print("Key areas to check:")
    print("1. Dialogue continuation not breaking incorrectly")
    print("2. Character (CONT'D) patterns recognized")
    print("3. Page numbers filtered out")
    print("4. Action properly separated from dialogue")

if __name__ == "__main__":
    run_all_tests()