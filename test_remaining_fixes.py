#!/usr/bin/env python3
"""
Test remaining parsing issues from Action_Spacing_Error.md
"""

from screenplay_parser import ScreenplayParser
import json

def test_remaining_issues():
    """Test remaining parsing issues that need fixing"""
    parser = ScreenplayParser()
    
    print("=== REMAINING PARSING ISSUES TEST ===\n")
    
    # Issue 1: Character name with missing dialogue (lines 185-187)
    print("1. CHARACTER NAME WITH MISSING DIALOGUE:")
    mock_character_data = [{
        'page_num': 1,
        'lines': [
            '                       DE-FI DOM (CONT\'D)',
            '',
            '           Patrick Weiss is in the house!',
            '',
            'Hannah locks on Patrick as he waves to the star-struck crowd.'
        ]
    }]
    
    scenes = parser._parse_sequential_content(mock_character_data)
    if scenes:
        content = scenes[0].get('content', '')
        lines = content.split('\n')
        print("Parsed result:")
        for i, line in enumerate(lines[:8]):
            leading_spaces = len(line) - len(line.lstrip()) if line else 0
            print(f"Line {i}: (spaces:{leading_spaces:2d}) '{line}'")
        print()
        
        # Check if character name and dialogue are properly paired
        has_char_name = any('DE-FI DOM (CONT\'D)' in line for line in lines)
        has_dialogue = any('Patrick Weiss is in the house' in line for line in lines)
        print(f"✅ Has character name: {has_char_name}")
        print(f"✅ Has dialogue: {has_dialogue}")
    print()
    
    # Issue 2: Scene elements spacing (lines 105-111)  
    print("2. SCENE ELEMENTS SPACING:")
    mock_scene_elements = [{
        'page_num': 1,
        'lines': [
            'WORK DESK',
            'Surrounded by stolen COMPUTER EQUIPMENT, HANNAH (24), a',
            'disaffected, rebellious MIT dropout, is intensely focused on',
            'soldering a microchip inside a GOLD PRADA WRISTBAND.',
            'ANGLE ON: Hannah\'s LAPTOP streams the DE-FI DOM YOUTUBE',
            'CHANNEL. (We will meet De-Fi Dom IRL later on.)'
        ]
    }]
    
    scenes = parser._parse_sequential_content(mock_scene_elements)
    if scenes:
        content = scenes[0].get('content', '')
        lines = content.split('\n')
        print("Scene elements parsing:")
        for i, line in enumerate(lines):
            leading_spaces = len(line) - len(line.lstrip()) if line else 0
            print(f"Line {i}: (spaces:{leading_spaces:2d}) '{line}'")
        print()
        
        # Check for blank lines around scene elements
        blank_lines = [i for i, line in enumerate(lines) if line.strip() == '']
        print(f"Blank line positions: {blank_lines}")
        print("✅ Scene elements should have blank lines for separation")
    print()
    
    # Issue 3: Dialogue appearing as action (lines 203-204)
    print("3. DIALOGUE CLASSIFIED AS ACTION:")
    mock_dialogue_action = [{
        'page_num': 1,
        'lines': [
            '                       BOUNCER',
            '           Don\'t look like it to me.',
            'Hannah rolls her smokey cat eyes.',
            'She\'s outta there.'
        ]
    }]
    
    scenes = parser._parse_sequential_content(mock_dialogue_action)
    if scenes:
        content = scenes[0].get('content', '')
        lines = content.split('\n')
        print("Dialogue vs action parsing:")
        for i, line in enumerate(lines):
            leading_spaces = len(line) - len(line.lstrip()) if line else 0 
            print(f"Line {i}: (spaces:{leading_spaces:2d}) '{line}'")
        print()
        
        # Check classification
        has_bouncer = any('BOUNCER' in line for line in lines)
        has_dialogue = any('Don\'t look like it to me' in line for line in lines)
        has_action = any('Hannah rolls her smokey' in line for line in lines)
        print(f"✅ Has BOUNCER character: {has_bouncer}")
        print(f"✅ Has dialogue: {has_dialogue}")  
        print(f"✅ Has Hannah action: {has_action}")

if __name__ == "__main__":
    test_remaining_issues()