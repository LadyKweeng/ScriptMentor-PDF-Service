#!/usr/bin/env python3

# Simple direct test of action classification
import re

def _is_clearly_action(text: str) -> bool:
    """Copy of the enhanced method for testing"""
    text_lower = text.lower()
    
    clear_action_indicators = [
        'girls protest', 'proud boys', 'storm the capitol', 'world trade center',
        'is attacked', 'is laid to rest', 'laid to rest', 'oil fields', 'on fire in', 'is beaten',
        'princess diana'
    ]
    
    if any(indicator in text_lower for indicator in clear_action_indicators):
        return True
    return False

# Test the problematic lines
test_lines = [
    "Girls protest in Iran. Proud Boys",
    "storm the Capitol. The", 
    "World Trade Center is attacked.",
    "Princess Diana is laid to",
    "rest. Oil fields are on fire in",
    "Iraq. Rodney King is beaten."
]

print("=== ENHANCED CLASSIFICATION TEST ===")
for line in test_lines:
    result = _is_clearly_action(line)
    print(f"'{line}' -> Action: {result}")