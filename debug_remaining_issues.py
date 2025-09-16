#!/usr/bin/env python3
"""
Debug the remaining parsing issues from Action_Spacing_Error.md
"""

from screenplay_parser import ScreenplayParser, ElementClassifier
import json

def debug_remaining_issues():
    """Debug specific remaining issues"""
    parser = ScreenplayParser()
    classifier = ElementClassifier()
    
    print("=== DEBUGGING REMAINING PARSING ISSUES ===\n")
    
    # Issue 1: Scene heading missing indentation (line 1)
    print("1. SCENE HEADING INDENTATION TEST:")
    scene_heading = "The view of our home two hundred and thirty-eight thousand miles away is majestic, peaceful, serene."
    print(f"Input: '{scene_heading}'")
    print(f"Is scene heading: {parser.patterns.is_scene_heading(scene_heading)}")
    print(f"Is action: {classifier._is_clearly_action(scene_heading)}")
    print(f"Should have action indentation (12 spaces)")
    print()
    
    # Issue 2: Dialogue continuation vs new action (lines 63-69)
    print("2. DIALOGUE CONTINUATION VS ACTION TEST:")
    dialogue_continuation_lines = [
        "Discord circle jerk of crypto bros",
        "getting off on multibillion-dollar", 
        "grifts. It's like a shit casino in",
        "Old Town Vegas with cheap vodka",
        "drinks and penny slots, and",
        "everyone who can count cards is",
        "there."
    ]
    
    for line in dialogue_continuation_lines:
        is_action = classifier._is_clearly_action(line)
        is_dialogue = classifier._is_likely_dialogue(line)
        print(f"'{line}'")
        print(f"  -> Action: {is_action}, Dialogue: {is_dialogue}")
        if is_action:
            print(f"     🚨 MISCLASSIFIED - Should be dialogue continuation")
        print()
    
    # Issue 3: Scene elements spacing (lines 105-111)
    print("3. SCENE ELEMENT DETECTION TEST:")
    scene_elements = [
        "WORK DESK",
        "Surrounded by stolen COMPUTER EQUIPMENT, HANNAH (24), a",
        "ANGLE ON: Hannah's LAPTOP streams the DE-FI DOM YOUTUBE",
        "CHANNEL. (We will meet De-Fi Dom IRL later on.)"
    ]
    
    for element in scene_elements:
        is_scene_element = element.isupper() and any(word in element for word in ['DESK', 'ANGLE ON', 'CHANNEL'])
        print(f"'{element}'")
        print(f"  -> Scene element: {is_scene_element}")
        if is_scene_element:
            print(f"     Should have blank line before/after")
        print()
        
    # Issue 4: Character name + dialogue parsing (lines 185-187)  
    print("4. CHARACTER NAME + DIALOGUE TEST:")
    character_dialogue_block = [
        "DE-FI DOM (CONT'D)",
        "",
        "Patrick Weiss is in the house!"
    ]
    
    for line in character_dialogue_block:
        is_char = parser.patterns.is_character_name(line)
        is_dialogue = classifier._is_likely_dialogue(line) 
        print(f"'{line}'")
        print(f"  -> Character: {is_char}, Dialogue: {is_dialogue}")
        print()

if __name__ == "__main__":
    debug_remaining_issues()