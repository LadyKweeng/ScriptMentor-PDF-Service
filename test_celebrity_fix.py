#!/usr/bin/env python3
"""
Test the celebrity action detection fix
"""

from screenplay_parser import ScreenplayParser

def test_celebrity_fix():
    """Test the enhanced celebrity action detection"""
    parser = ScreenplayParser()
    
    # Test with the exact problematic content
    mock_data = [{
        'page_num': 1,
        'lines': [
            '                                      HANNAH (V.O.)',
            '                         The metaverse... A pyramid scheme',
            '                         for twenty-something kleptocrats. A',
            '                         Discord circle jerk of crypto bros',
            '                         getting off on multibillion-dollar',
            '                         grifts. It\'s like a shit casino in',
            '                         Old Town Vegas with cheap vodka',
            '                         drinks and penny slots, and',
            '                         everyone who can count cards is',
            '                         there.',
            '                         Dan Bilzerian jet skis. Jeff Bezos',
            '                         emerges from his',
            '                         spaceship. Elon Musk smokes weed on',
            '                         the Joe Rogan Podcast.',
            '',
            '            The Antarctic ice shelf collapses into the ocean.'
        ]
    }]
    
    print("=== TESTING CELEBRITY ACTION FIX ===\n")
    
    try:
        scenes = parser._parse_sequential_content(mock_data)
        
        if scenes:
            content = scenes[0].get('content', '')
            print("Enhanced parsing results:")
            lines = content.split('\n')
            
            for i, line in enumerate(lines):
                leading_spaces = len(line) - len(line.lstrip()) if line else 0
                marker = " 👈 FIXED!" if 'dan bilzerian' in line.lower() and leading_spaces == 12 else ""
                marker = marker or (" ❌ STILL WRONG" if 'dan bilzerian' in line.lower() and leading_spaces == 25 else "")
                print(f"Line {i:2d}: (spaces:{leading_spaces:2d}) '{line[:60]}{'...' if len(line) > 60 else ''}'{marker}")
            
            # Check for the specific fix
            dan_line = next((line for line in lines if 'dan bilzerian' in line.lower()), None)
            if dan_line:
                spaces = len(dan_line) - len(dan_line.lstrip())
                if spaces == 12:
                    print(f"\n✅ SUCCESS: 'Dan Bilzerian jet skis...' now classified as ACTION (12 spaces)")
                elif spaces == 25:
                    print(f"\n❌ STILL BROKEN: 'Dan Bilzerian jet skis...' still classified as DIALOGUE (25 spaces)")
                else:
                    print(f"\n⚠️ UNEXPECTED: 'Dan Bilzerian jet skis...' has {spaces} spaces")
            else:
                print(f"\n❓ MISSING: Could not find 'Dan Bilzerian' line in output")
                
        else:
            print("❌ No scenes returned")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_celebrity_fix()