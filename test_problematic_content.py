#!/usr/bin/env python3
"""
Test with the exact problematic content from Action_Spacing_Error.md
"""

from screenplay_parser import ScreenplayParser
import json

def test_problematic_content():
    """Test with content that should show the dialogue/action confusion"""
    parser = ScreenplayParser()
    
    # Extract the exact problematic section from Action_Spacing_Error.md
    mock_data = [{
        'page_num': 1,
        'lines': [
            # Lines 100-114 from Action_Spacing_Error.md where the problem occurs
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
            '                         Dan Bilzerian jet skis. Jeff Bezos',
            '                         emerges from his',
            '                         spaceship. Elon Musk smokes weed on',
            '                         the Joe Rogan Podcast.',
            '',
            '            The Antarctic ice shelf collapses into the ocean.',
            '',
            '                                      HANNAH (V.O.)',
            '                         And when the world\'s largest multi-'
        ]
    }]
    
    print("=== TESTING PROBLEMATIC CONTENT ===\n")
    
    try:
        scenes = parser._parse_sequential_content(mock_data)
        
        if scenes:
            content = scenes[0].get('content', '')
            print("Parsed content:")
            lines = content.split('\n')
            for i, line in enumerate(lines):
                leading_spaces = len(line) - len(line.lstrip()) if line else 0
                print(f"Line {i:2d}: (spaces:{leading_spaces:2d}) '{line}'")
                
        else:
            print("❌ No scenes returned")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_problematic_content()