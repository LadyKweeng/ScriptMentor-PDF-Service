#!/usr/bin/env python3
"""
Test the Railway API directly to see what it returns
"""

import requests
import json
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
import os

def create_test_pdf():
    """Create a test PDF with the problematic content"""
    # Create PDF in memory
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Add the problematic content with proper spacing
    y_position = height - 50
    line_height = 14
    
    lines = [
        "            The view of our home two hundred and thirty-eight thousand miles away is majestic, peaceful, serene.",
        "",
        "",
        "                                      HANNAH (V.O.)",
        "                         Welcome to the metaverse. The",
        "                         single most important evolution in", 
        "                         technology since the invention of",
        "                         the wheel. The greatest re-",
        "                         distribution of wealth in human",
        "                         history. A time unlike any other,",
        "                         where the little guy will finally",
        "                         get a piece of the pie... That's",
        "                         the pitch, anyway.",
        "",
        "            As we push in on Planet Earth, a precipitous montage of",
        "            significant global events unfolds. We see the truth. Our",
        "            truth. The reality of our world as we know it.",
        "",
        "                                      HANNAH (V.O.)",
        "                         But what all this clickbait PR",
        "                         really means is the already rich",
        "                         are just fleecing the perpetual",
        "                         poor. A techno-feudal Ponzi scheme",
        "                         where somebody wins and everybody",
        "                         else can fuck right off.",
        "            Girls protest in Iran. Proud Boys storm the Capitol. The",
        "            World Trade Center is attacked. Princess Diana is laid to",
        "            rest. Oil fields are on fire in Iraq. Rodney King is beaten."
    ]
    
    for line in lines:
        if line.strip():  # Skip empty lines for PDF
            c.drawString(50, y_position, line)
        y_position -= line_height
    
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

def test_railway_api():
    """Test the Railway API with our test content"""
    print("=== TESTING RAILWAY API ===\n")
    
    # Create test PDF
    pdf_data = create_test_pdf()
    
    # Save to temp file for upload
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
        tmp.write(pdf_data)
        tmp_path = tmp.name
    
    try:
        # Test API
        url = "http://localhost:5000/parse-screenplay"
        
        with open(tmp_path, 'rb') as f:
            files = {'file': ('test.pdf', f, 'application/pdf')}
            response = requests.post(url, files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ API Response Success!")
            print(f"Status: {response.status_code}")
            print(f"Processing info: {result.get('metadata', {}).get('processedVia', 'N/A')}")
            print(f"Scenes found: {len(result.get('scenes', []))}")
            
            # Examine first scene content
            if result.get('scenes'):
                scene = result['scenes'][0]
                content = scene.get('content', '')
                print(f"\nFirst scene content (first 10 lines):")
                lines = content.split('\n')
                for i, line in enumerate(lines[:10]):
                    leading_spaces = len(line) - len(line.lstrip()) if line else 0
                    print(f"Line {i:2d}: (spaces:{leading_spaces:2d}) '{line[:80]}{'...' if len(line) > 80 else ''}'")
                
                print(f"\nTotal content lines: {len(lines)}")
                print(f"Scene heading: '{scene.get('heading', 'NO HEADING')}'")
                
                # Save full response for inspection
                with open('api_response.json', 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"\n📄 Full API response saved to: api_response.json")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

if __name__ == "__main__":
    test_railway_api()