#!/usr/bin/env python3
"""
Test enhanced linguistic pattern detection for dialogue vs action classification
"""

from screenplay_parser import ScreenplayParser

def test_linguistic_patterns():
    """Test the enhanced linguistic pattern detection"""
    parser = ScreenplayParser()
    
    print("=== TESTING ENHANCED LINGUISTIC PATTERN DETECTION ===\n")
    
    # Test cases: dialogue style vs action style
    test_cases = [
        {
            'description': 'DIALOGUE STYLE (first-person, conversational)',
            'lines': [
                "I'm talking about crypto.",
                "And no, I'm not talking about the stock market.",
                "But what all this clickbait PR really means is the already rich are just fleecing the perpetual poor.",
                "It's like a shit casino in Old Town Vegas with cheap vodka drinks."
            ],
            'expected_type': 'dialogue'
        },
        {
            'description': 'ACTION STYLE (third-person, descriptive/narrative)',
            'lines': [
                "Dan Bilzerian jet skis. Jeff Bezos emerges from his spaceship.",
                "Hannah walks into the room and sits down.",
                "The view of our home two hundred miles away is majestic.",
                "Girls protest in Iran. Proud Boys storm the Capitol.",
                "He opens his phone and checks his wallet.",
                "Roger holds the joint up and takes a hit.",
                "The Antarctic ice shelf collapses into the ocean."
            ],
            'expected_type': 'action'
        },
        {
            'description': 'MIXED CONTEXT TEST (dialogue that shifts to action)',
            'lines': [
                '                                      HANNAH (V.O.)',
                '                         The metaverse... A pyramid scheme',
                '                         for twenty-something kleptocrats. A',
                '                         Discord circle jerk of crypto bros',
                '                         getting off on multibillion-dollar',
                '                         grifts. It\'s like a shit casino in',
                '                         Old Town Vegas with cheap vodka',
                '                         drinks and penny slots, and',
                '                         everyone who can count cards is',
                '                         there.',
                '                         Dan Bilzerian jet skis. Jeff Bezos',  # <- Should break dialogue here
                '                         emerges from his',
                '                         spaceship. Elon Musk smokes weed on',
                '                         the Joe Rogan Podcast.'
            ],
            'expected_type': 'mixed'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"{i}. {test_case['description']}:")
        print("-" * 50)
        
        if test_case['expected_type'] == 'mixed':
            # Test the full mixed context scenario
            mock_data = [{'page_num': 1, 'lines': test_case['lines']}]
            try:
                scenes = parser._parse_sequential_content(mock_data)
                if scenes:
                    content = scenes[0].get('content', '')
                    lines = content.split('\n')
                    
                    for j, line in enumerate(lines):
                        leading_spaces = len(line) - len(line.lstrip()) if line else 0
                        line_type = "CHARACTER" if leading_spaces == 38 else ("DIALOGUE" if leading_spaces == 25 else ("ACTION" if leading_spaces == 12 else "OTHER"))
                        
                        if 'dan bilzerian' in line.lower():
                            if leading_spaces == 12:
                                print(f"  Line {j:2d}: (spaces:{leading_spaces:2d}) {line_type} '{line[:50]}...' ✅ CORRECTLY DETECTED AS ACTION")
                            else:
                                print(f"  Line {j:2d}: (spaces:{leading_spaces:2d}) {line_type} '{line[:50]}...' ❌ INCORRECTLY CLASSIFIED")
                        elif line.strip():
                            print(f"  Line {j:2d}: (spaces:{leading_spaces:2d}) {line_type} '{line[:50]}...'")
                            
            except Exception as e:
                print(f"  ❌ Error: {e}")
        else:
            # Test individual lines for dialogue vs action style detection
            for line in test_case['lines']:
                is_narrative = parser.classifier._is_narrative_action_style(line)
                result = "ACTION" if is_narrative else "DIALOGUE"
                expected = test_case['expected_type'].upper()
                status = "✅" if result == expected else "❌"
                print(f"  '{line[:60]}...' -> {result} {status}")
        
        print("\n")
    
    # Test specific patterns
    print("4. SPECIFIC LINGUISTIC PATTERN TESTS:")
    print("-" * 50)
    
    specific_tests = [
        ("Dan Bilzerian jet skis across the water.", "ACTION - Proper noun + action verb"),
        ("Girls protest in Iran for women's rights.", "ACTION - Proper noun sequence + action"),
        ("The view of our home is beautiful.", "ACTION - Definite article + descriptive"),
        ("He opens his phone and checks the screen.", "ACTION - Third-person + possessive"),
        ("But what I really mean is different.", "DIALOGUE - First-person conversational"),
        ("And no, I'm not talking about that.", "DIALOGUE - First-person with negation"),
        ("It's like a casino with cheap drinks.", "DIALOGUE - Conversational comparison"),
        ("Roger holds the joint up.", "ACTION - Name + action verb"),
        ("She walks into the room.", "ACTION - Pronoun + movement verb")
    ]
    
    for text, expected in specific_tests:
        is_narrative = parser.classifier._is_narrative_action_style(text)
        result = "ACTION" if is_narrative else "DIALOGUE"
        expected_type = expected.split(" - ")[0]
        status = "✅" if result == expected_type else "❌"
        reason = expected.split(" - ")[1] if " - " in expected else ""
        print(f"  '{text}' -> {result} {status} ({reason})")

if __name__ == "__main__":
    test_linguistic_patterns()