#!/usr/bin/env python3
"""
Quick debug to see what's happening with the parsing
"""

from screenplay_parser import ScreenplayParser
import json

def quick_debug():
    """Quick debug of current parsing behavior"""
    parser = ScreenplayParser()
    
    # Test with the problematic content from Action_Spacing_Error.md
    mock_data = [{
        'page_num': 1,
        'lines': [
            'The view of our home two hundred and thirty-eight thousand miles away is majestic, peaceful, serene.',
            '',
            '',
            '                       HANNAH (V.O.)',
            '           Welcome to the metaverse. The',
            '           single most important evolution in',
            '           technology since the invention of',
            '           the wheel. The greatest re-',
            '           distribution of wealth in human',
            '           history. A time unlike any other,',
            '           where the little guy will finally',
            '           get a piece of the pie... That\'s',
            '           the pitch, anyway.',
            '',
            'As we push in on Planet Earth, a precipitous montage of',
            'significant global events unfolds. We see the truth. Our',
            'truth. The reality of our world as we know it.',
            '',
            '                       HANNAH (V.O.)',
            '           But what all this clickbait PR',
            '           really means is the already rich',
            '           are just fleecing the perpetual',
            '           poor. A techno-feudal Ponzi scheme',
            '           where somebody wins and everybody',
            '           else can fuck right off.',
            'Girls protest in Iran. Proud Boys storm the Capitol. The',
            'World Trade Center is attacked. Princess Diana is laid to',
            'rest. Oil fields are on fire in Iraq. Rodney King is beaten.'
        ]
    }]
    
    print("=== CURRENT PARSING DEBUG ===\n")
    
    try:
        scenes = parser._parse_sequential_content(mock_data)
        
        if scenes:
            content = scenes[0].get('content', '')
            print("First 20 lines of parsed content:")
            lines = content.split('\n')
            for i, line in enumerate(lines[:20]):
                leading_spaces = len(line) - len(line.lstrip()) if line else 0
                print(f"Line {i:2d}: (spaces:{leading_spaces:2d}) '{line}'")
            
            print(f"\nTotal lines: {len(lines)}")
            print(f"Scene heading: '{scenes[0].get('heading', 'NO HEADING')}'")
            
        else:
            print("❌ No scenes returned")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    quick_debug()