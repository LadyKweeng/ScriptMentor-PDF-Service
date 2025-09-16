#!/usr/bin/env python3
"""
Debug scene heading detection
"""

from screenplay_parser import EnhancedScreenplayPatterns, ElementClassifier

def debug_scene_detection():
    """Debug why scene detection might be failing"""
    patterns = EnhancedScreenplayPatterns()
    classifier = ElementClassifier()
    
    print("=== SCENE DETECTION DEBUG ===\n")
    
    # Test potential scene headings
    test_lines = [
        "The view of our home two hundred and thirty-eight thousand miles away is majestic, peaceful, serene.",
        "INT. NIGHTCLUB - NEW YORK CITY - NIGHT",
        "EXT. TIMES SQUARE - NEW YORK CITY - NIGHT", 
        "INT. HANNAH'S WORKSPACE - NEW YORK CITY - NIGHT"
    ]
    
    for line in test_lines:
        is_scene = patterns.is_scene_heading(line)
        classification = classifier.classify_line(line, 0, [line])
        print(f"Line: '{line[:50]}...'")
        print(f"  is_scene_heading: {is_scene}")
        print(f"  classifier type: {classification.get('type', 'UNKNOWN')}")
        print()
        
    # Check if there might be an infinite loop or hanging
    print("=== TESTING BASIC PARSING ===")
    
    # Very simple test data
    simple_data = [{
        'page_num': 1,
        'lines': [
            'INT. TEST SCENE - DAY',
            '',
            'This is action text.',
            '',
            '                       CHARACTER',
            '           This is dialogue.'
        ]
    }]
    
    try:
        from screenplay_parser import ScreenplayParser
        parser = ScreenplayParser()
        
        print("Testing with simple scene...")
        # Try just the scene detection part
        scenes_found = []
        
        for page_data in simple_data:
            for line in page_data['lines']:
                if patterns.is_scene_heading(line.strip()):
                    scenes_found.append(line.strip())
                    
        print(f"Scene headings found: {scenes_found}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_scene_detection()