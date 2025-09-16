#!/usr/bin/env python3
"""
Core issue debugging for Action_Spacing_Error.md problems
"""

from screenplay_parser import ScreenplayParser, ElementClassifier, EnhancedScreenplayPatterns
import json

def debug_core_issues():
    """Debug the core parsing issues"""
    classifier = ElementClassifier()
    patterns = EnhancedScreenplayPatterns()
    
    print("=== CORE PARSING ISSUES ANALYSIS ===\n")
    
    # Issue 1: Opening line missing indentation
    print("1. OPENING LINE INDENTATION:")
    opening_line = "The view of our home two hundred and thirty-eight thousand miles away is majestic, peaceful, serene."
    print(f"Input: '{opening_line[:50]}...'")
    print(f"Is scene heading: {patterns.is_scene_heading(opening_line)}")
    print(f"Is action: {classifier._is_clearly_action(opening_line)}")
    print("✅ FINDING: Should be action with 12-space indentation")
    print()
    
    # Issue 2: Dialogue continuation being parsed as action
    print("2. DIALOGUE CONTINUATION PROBLEM:")
    dialogue_lines = [
        "Discord circle jerk of crypto bros",
        "getting off on multibillion-dollar", 
        "grifts. It's like a shit casino in"
    ]
    
    for line in dialogue_lines:
        is_action = classifier._is_clearly_action(line)
        print(f"'{line}'")
        print(f"  -> Classified as action: {is_action}")
        if is_action:
            print("  🚨 ERROR: Should be dialogue continuation with 25-space indentation")
        else:
            print("  ✅ CORRECT: Should be dialogue continuation")
        print()
    
    # Issue 3: Missing character dialogue
    print("3. CHARACTER DIALOGUE PARSING:")
    char_line = "DE-FI DOM (CONT'D)"
    dialogue_line = "Patrick Weiss is in the house!"
    print(f"Character: '{char_line}'")
    print(f"Is character name: {patterns.is_character_name(char_line)}")
    print(f"Dialogue: '{dialogue_line}'")  
    print(f"Is action: {classifier._is_clearly_action(dialogue_line)}")
    print("✅ Should be: Character name (38 spaces) + Dialogue (25 spaces)")
    print()
    
    # Issue 4: Action keywords causing misclassification
    print("4. ACTION KEYWORD ANALYSIS:")
    problematic_words = ['circle jerk', 'crypto bros', 'casino', 'vodka drinks']
    
    for phrase in problematic_words:
        test_line = f"some {phrase} content here"
        is_action = classifier._is_clearly_action(test_line)
        print(f"'{phrase}' -> triggers action classification: {is_action}")
    
    print("\n=== SOLUTION STRATEGIES ===")
    print("1. First line should get action indentation - ✅ Working")
    print("2. Need context-aware dialogue continuation detection")  
    print("3. Need proper character name + dialogue pairing")
    print("4. Some action patterns may be too broad for dialogue context")

if __name__ == "__main__":
    debug_core_issues()