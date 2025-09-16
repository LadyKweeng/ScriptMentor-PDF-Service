#!/usr/bin/env python3
"""
Test the context-aware dialogue continuation fix
"""

from screenplay_parser import ElementClassifier

def test_context_awareness():
    """Test dialogue continuation with context awareness"""
    classifier = ElementClassifier()
    
    print("=== CONTEXT-AWARE DIALOGUE CONTINUATION TEST ===\n")
    
    # Simulate dialogue block context
    print("1. SETTING UP DIALOGUE CONTEXT:")
    classifier.in_dialogue_block = True
    classifier.last_element = 'dialogue'
    print("✅ in_dialogue_block = True")
    print("✅ last_element = 'dialogue'")
    print()
    
    # Test the problematic lines
    print("2. TESTING PROBLEMATIC DIALOGUE CONTINUATION:")
    dialogue_lines = [
        "Discord circle jerk of crypto bros",
        "getting off on multibillion-dollar", 
        "grifts. It's like a shit casino in",
        "Old Town Vegas with cheap vodka",
        "drinks and penny slots, and",
        "everyone who can count cards is",
        "there."
    ]
    
    for line in dialogue_lines:
        is_action = classifier._is_clearly_action(line)
        print(f"'{line}'")
        print(f"  -> Should break dialogue: {is_action}")
        if is_action:
            print("  🚨 PROBLEM: Still breaking dialogue")
        else:
            print("  ✅ CORRECT: Continuing dialogue")
        print()
    
    # Test strong action that should break dialogue
    print("3. TESTING STRONG ACTION THAT SHOULD BREAK DIALOGUE:")
    strong_action_lines = [
        "Hannah walks to the door.",
        "ANGLE ON: The computer screen.",
        "We see the destruction.",
        "WORK DESK",
        "The view of our planet is amazing."
    ]
    
    for line in strong_action_lines:
        is_action = classifier._is_clearly_action(line)
        print(f"'{line}'")
        print(f"  -> Should break dialogue: {is_action}")
        if is_action:
            print("  ✅ CORRECT: Strong action breaks dialogue")
        else:
            print("  ❓ UNEXPECTED: Should break dialogue")
        print()

if __name__ == "__main__":
    test_context_awareness()