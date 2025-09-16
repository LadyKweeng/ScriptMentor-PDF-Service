#!/usr/bin/env python3
"""
Test action formatting to see what the Railway service actually outputs
"""

from screenplay_parser import ScreenplayParser
import json

def test_action_formatting():
    """Test the actual action formatting output"""
    parser = ScreenplayParser()
    
    # Simulate the problematic content from Action_Spacing_Error.md
    mock_pages_data = [{
        'page_num': 1,
        'lines': [
            'INT. NIGHTCLUB - NEW YORK CITY - NIGHT',
            '',
            "HANNAH'S SUMMER SONG continues throughout the club.",
            "Buzzing lasers and raver-clad DANCERS spinning TECHNICOLORED",
            "HULA HOOPS frame a giant LED SCREEN animating poorly-rendered",
            "CRYPTO ART.",
            "Hannah scans the madhouse of CRYPTO BROS, and E-GIRLS. Her",
            "intense focus is unbroken by the MECHANICAL BULL revving into",
            "action, bucking off one douchebag after another.",
            "DE-FI DOM (25), slicked hair and a slippery charisma,",
            "YouTube's biggest crypto influencer, hovers next to the DIPLO",
            "LOOK-ALIKE DJ. He grabs the mic.",
            '',
            '',
            '                       DE-FI DOM',
            '           NEW YORK CITY! Everyone having a',
            '           good time?',
            '',
            '                       CROWD',
            '           Yeah!',
            '',
            '                       DE-FI DOM',
            '           Let\'s celebrate this guy over here',
            '           for making it happen. The OG',
            '           himself...',
            'De-Fi Dom points to PATRICK WEISS',
            '(30s), trust-funder turned',
            'crypto billionaire. Don\'t be fooled',
            'by this guy\'s heart-',
            'melting smile; dark triad is an',
            'understatement.',
            '           DE-FI DOM (CONT\'D)',
            '           Patrick Weiss is in the house!',
            'Hannah locks on Patrick as he waves',
            'to the star-struck crowd.',
            '',
            'Girls protest in Iran. Proud Boys',
            'storm the Capitol. The',
            'World Trade Center is attacked.',
            'Princess Diana is laid to',
            'rest. Oil fields are on fire in',
            'Iraq. Rodney King is beaten.',
            '',
            '                       HANNAH (V.O.)',
            '           And in this scorched-earth',
            '           hellscape of economic catastrophe,',
            '           stripped bare by the boomer',
            '           generation, you\'re either of two',
            '           people -- the one cheating,',
            '           scamming, screwing over your',
            '           friends or the one getting screwed.',
            '           Either way, we\'re doomed.'
        ]
    }]
    
    # Test the sequential content parsing (this is what creates structured data)
    scenes = parser._parse_sequential_content(mock_pages_data)
    
    print("=== BACKEND STRUCTURED DATA OUTPUT ===")
    if scenes:
        first_scene = scenes[0]
        print(f"Scene heading: '{first_scene.get('heading', 'NO HEADING')}'")
        print(f"\nScene content (first 500 chars):\n'{first_scene.get('content', 'NO CONTENT')[:500]}...'")
        
        # Check specific issues
        content = first_scene.get('content', '')
        print(f"\n=== ACTION SPACING ANALYSIS ===")
        print(f"Contains 'HANNAH SUMMER SONG': {'HANNAH' in content and 'SUMMER SONG' in content}")
        print(f"Contains 'Buzzing lasers': {'Buzzing lasers' in content}")
        print(f"Contains 'De-Fi Dom points to': {'De-Fi Dom points to' in content}")
        
        # Check if there are blank lines between these sections
        lines = content.split('\n')
        for i, line in enumerate(lines[:10]):
            print(f"Line {i}: '{line}'")
    
    # Also test element detection directly with mock data
    print(f"\n=== ELEMENTS BEFORE FORMATTING ===")
    elements = parser._detect_elements(mock_pages_data)
    
    action_elements = [e for e in elements if e['type'] == 'action']
    dialogue_elements = [e for e in elements if e['type'] == 'dialogue']
    
    print(f"Action elements: {len(action_elements)}")
    print(f"Dialogue elements: {len(dialogue_elements)}")
    
    print("\nFirst few elements:")
    for i, element in enumerate(elements[:15]):
        print(f"{i}: {element['type']} - '{element['text']}'")

if __name__ == "__main__":
    test_action_formatting()