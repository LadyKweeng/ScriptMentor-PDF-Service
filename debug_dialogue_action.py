#!/usr/bin/env python3
"""
Debug the specific dialogue/action issue
"""

from screenplay_parser import ElementClassifier

def debug_dialogue_action():
    """Debug why 'As we push in on Planet Earth' isn't breaking dialogue"""
    classifier = ElementClassifier()
    
    print("=== DIALOGUE vs ACTION DEBUG ===\n")
    
    # Set up dialogue context
    classifier.in_dialogue_block = True
    classifier.last_element = 'dialogue'
    
    problematic_line = "As we push in on Planet Earth, a precipitous montage of"
    
    print(f"Testing: '{problematic_line}'")
    print(f"in_dialogue_block: {classifier.in_dialogue_block}")
    print(f"last_element: {classifier.last_element}")
    
    # Check if it's considered clear action
    is_clear_action = classifier._is_clearly_action(problematic_line)
    print(f"_is_clearly_action: {is_clear_action}")
    
    # Check the strong dialogue breakers
    text_lower = problematic_line.lower()
    strong_dialogue_breakers = [
        'hannah walks', 'hannah moves', 'hannah enters', 'hannah exits',
        'she walks', 'he walks', 'she moves', 'he moves', 'she enters', 'he enters',
        'angle on', 'close on', 'wide shot', 'work desk', 'clothing rack',
        'the view of', 'we see', 'we witness', 'fade in', 'fade out', 'cut to'
    ]
    
    print(f"\nChecking dialogue breakers:")
    for breaker in strong_dialogue_breakers:
        if breaker in text_lower:
            print(f"  ✅ Found: '{breaker}'")
    
    # The issue is 'as we push in' should match 'we' patterns
    print(f"\nSpecific checks:")
    print(f"  'we' in text: {'we' in text_lower}")
    print(f"  'push in' in text: {'push in' in text_lower}")
    print(f"  'as we push in' in text: {'as we push in' in text_lower}")
    
    # Test what should happen
    print(f"\nThis should be ACTION because it's a camera direction")
    print(f"'As we push in' = camera movement = should break dialogue")

if __name__ == "__main__":
    debug_dialogue_action()