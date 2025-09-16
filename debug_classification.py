#!/usr/bin/env python3
"""
Debug specific classification issue with "Girls protest in Iran" content
"""

from screenplay_parser import ScreenplayParser
import json

def debug_specific_issue():
    """Debug the exact problematic content from Action_Spacing_Error.md"""
    parser = ScreenplayParser()
    
    # Mock the specific problematic content from Action_Spacing_Error.md lines 29-42
    mock_pages_data = [{
        'page_num': 1,
        'lines': [
            '                       HANNAH (V.O.)',
            '           But what all this clickbait PR',
            '           really means is the already rich',
            '           are just fleecing the perpetual',
            '           poor. A techno-feudal Ponzi scheme',
            '           where somebody wins and everybody',
            '           else can fuck right off.',
            '           Girls protest in Iran. Proud Boys',
            '           storm the Capitol. The',
            '           World Trade Center is attacked.',
            '           Princess Diana is laid to',
            '           rest. Oil fields are on fire in',
            '           Iraq. Rodney King is beaten.',
            '',
            '                       HANNAH (V.O.)',
            '           And in this scorched-earth',
            '           hellscape of economic catastrophe,'
        ]
    }]
    
    # Test the sequential content parsing
    scenes = parser._parse_sequential_content(mock_pages_data)
    
    if scenes:
        scene_content = scenes[0].get('content', '')
        lines = scene_content.split('\n')
        
        print("=== SCENE CONTENT ANALYSIS ===")
        print("Full content:")
        for i, line in enumerate(lines):
            leading_spaces = len(line) - len(line.lstrip())
            print(f"Line {i:2d}: (spaces:{leading_spaces:2d}) '{line}'")
        
        print("\n=== CLASSIFICATION ANALYSIS ===")
        
        # Check the specific problematic lines
        problem_lines = [
            "Girls protest in Iran. Proud Boys",
            "storm the Capitol. The", 
            "World Trade Center is attacked.",
            "Princess Diana is laid to",
            "rest. Oil fields are on fire in",
            "Iraq. Rodney King is beaten."
        ]
        
        for line in problem_lines:
            # Test if classified as action
            is_action = parser._is_clearly_action(line)
            is_dialogue = parser._is_likely_dialogue(line)
            print(f"'{line}'")
            print(f"  -> Action: {is_action}, Dialogue: {is_dialogue}")
            
            # Check specific patterns
            if 'protest' in line.lower():
                print(f"     Contains 'protest' - should be action")
            if 'storm the Capitol' in line:
                print(f"     Contains 'storm the Capitol' - should be action")
            if 'attacked' in line.lower():
                print(f"     Contains 'attacked' - should be action")

if __name__ == "__main__":
    debug_specific_issue()