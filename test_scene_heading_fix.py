#!/usr/bin/env python3
"""
Quick test to verify scene heading indentation fix
"""

from screenplay_parser import ScreenplayParser

def test_scene_heading_indentation():
    """Test that scene headings get proper 1.5\" margin"""
    parser = ScreenplayParser()
    
    # Create mock pages data with a scene heading
    mock_pages_data = [{
        'page_num': 1,
        'lines': [
            'EXT. PLANET EARTH - PRESENT DAY',  # This should be detected as scene heading
            '',
            'The view of our home is majestic.',  # This should be action
        ]
    }]
    
    # Test the sequential content parsing
    scenes = parser._parse_sequential_content(mock_pages_data)
    
    print("=== SCENE HEADING INDENTATION TEST ===")
    print(f"Number of scenes detected: {len(scenes)}")
    
    if scenes:
        first_scene = scenes[0]
        heading = first_scene.get('heading', 'NO HEADING FOUND')
        print(f"Scene heading: '{heading}'")
        print(f"Starts with 12 spaces: {heading.startswith('            ')}")
        print(f"Length of leading spaces: {len(heading) - len(heading.lstrip())}")
        
        content = first_scene.get('content', 'NO CONTENT FOUND')
        print(f"Scene content preview: '{content[:50]}...'")
    else:
        print("❌ No scenes detected!")
    
    print("\n=== EXPECTED vs ACTUAL ===")
    print("Expected: '            EXT. PLANET EARTH - PRESENT DAY'")
    if scenes:
        print(f"Actual:   '{scenes[0].get('heading', 'NO HEADING')}'")
        
    return scenes

if __name__ == "__main__":
    test_scene_heading_indentation()