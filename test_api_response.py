#!/usr/bin/env python3
"""
Test the actual API response structure for scene headings
"""

from screenplay_parser import ScreenplayParser
import json

def test_api_response_structure():
    """Test what the API actually returns for scene headings"""
    parser = ScreenplayParser()
    
    # Create mock pages data with a scene heading
    mock_pages_data = [{
        'page_num': 1,
        'lines': [
            'EXT. PLANET EARTH - PRESENT DAY',
            '',
            'The view of our home is majestic.',
        ]
    }]
    
    # Simulate the full API parsing pipeline
    # This is what gets returned by parse_pdf() → _format_for_scriptorly()
    metadata = {'title': 'Test Script', 'pages': 1}
    quality = {'overallScore': 0.95}
    total_pages = 1
    
    # Get the actual API response structure
    api_response = parser._format_for_scriptorly(metadata, mock_pages_data, quality, total_pages)
    
    print("=== ACTUAL API RESPONSE STRUCTURE ===")
    print(json.dumps(api_response, indent=2)[:1000] + "...")
    
    print("\n=== SCENE DATA SPECIFICALLY ===")
    if api_response.get('scenes'):
        first_scene = api_response['scenes'][0]
        print(f"Scene heading field: '{first_scene.get('heading', 'NO HEADING')}'")
        print(f"Scene content field: '{first_scene.get('content', 'NO CONTENT')[:100]}...'")
        
        # Check if heading has indentation
        heading = first_scene.get('heading', '')
        if heading:
            leading_spaces = len(heading) - len(heading.lstrip())
            print(f"Scene heading leading spaces: {leading_spaces}")
            print(f"Scene heading starts with 12 spaces: {heading.startswith('            ')}")
    
    return api_response

if __name__ == "__main__":
    test_api_response_structure()