#!/usr/bin/env python3
"""
Simple test script for Railway PDF service functionality
"""

import os
import tempfile
from app import app
import json

def test_health_endpoint():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    
    app.config['TESTING'] = True
    with app.test_client() as client:
        response = client.get('/health')
        
        if response.status_code == 200:
            print("✅ Health endpoint working")
            data = response.get_json()
            print(f"   Service: {data.get('service')}")
            print(f"   Status: {data.get('status')}")
            print(f"   pdfplumber Ready: {data.get('pdfplumber_ready')}")
            return True
        else:
            print(f"❌ Health endpoint failed with status {response.status_code}")
            return False

def test_import_dependencies():
    """Test that all required dependencies can be imported"""
    print("\n🔍 Testing dependency imports...")
    
    try:
        import pdfplumber
        print("✅ pdfplumber imported successfully")
        
        import reportlab
        print("✅ reportlab imported successfully")
        
        from utils.pattern_enhancer import EnhancedScreenplayPatterns
        print("✅ pattern_enhancer imported successfully")
        
        from utils.quality_calculator import QualityCalculator
        print("✅ quality_calculator imported successfully")
        
        from screenplay_parser import ScreenplayParser
        print("✅ screenplay_parser imported successfully")
        
        from fdx_converter import FDXToPDFConverter
        print("✅ fdx_converter imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_pattern_recognition():
    """Test pattern recognition functionality"""
    print("\n🔍 Testing pattern recognition...")
    
    try:
        from utils.pattern_enhancer import EnhancedScreenplayPatterns
        patterns = EnhancedScreenplayPatterns()
        
        # Test scene heading detection
        scene_tests = [
            ("INT. KITCHEN - DAY", True),
            ("EXT. STREET - NIGHT", True),
            ("This is regular dialogue", False),
            ("CHARACTER NAME", False)
        ]
        
        for text, expected in scene_tests:
            result = patterns.is_scene_heading(text)
            if result == expected:
                print(f"   ✅ Scene detection: '{text}' -> {result}")
            else:
                print(f"   ❌ Scene detection failed: '{text}' -> {result} (expected {expected})")
                return False
        
        # Test character name detection
        char_tests = [
            ("JOHN", True),
            ("SARAH (O.S.)", True),
            ("FADE IN", False),
            ("This is dialogue", False)
        ]
        
        for text, expected in char_tests:
            result = patterns.is_character_name(text)
            if result == expected:
                print(f"   ✅ Character detection: '{text}' -> {result}")
            else:
                print(f"   ❌ Character detection failed: '{text}' -> {result} (expected {expected})")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Pattern recognition test failed: {e}")
        return False

def test_quality_calculator():
    """Test quality calculation functionality"""
    print("\n🔍 Testing quality calculator...")
    
    try:
        from utils.quality_calculator import QualityCalculator
        calc = QualityCalculator()
        
        # Mock data for testing
        class MockPDF:
            pages = [1, 2, 3]  # 3 pages
            
        mock_pages = [
            {'lines': ['line1', 'line2'], 'word_count': 10},
            {'lines': ['line3', 'line4'], 'word_count': 15},
            {'lines': ['line5'], 'word_count': 5}
        ]
        
        scenes = ['INT. ROOM - DAY', 'EXT. STREET - NIGHT']
        characters = {'JOHN', 'SARAH'}
        dialogue_blocks = ['Hello there', 'How are you?']
        action_blocks = ['John walks in', 'Sarah smiles']
        
        result = calc.calculate_quality(
            MockPDF(), mock_pages, scenes, characters, dialogue_blocks, action_blocks
        )
        
        if 'overallScore' in result and 'metrics' in result:
            print(f"   ✅ Quality calculation successful")
            print(f"   Overall Score: {result['overallScore']}")
            print(f"   Total Pages: {result['metrics']['totalPages']}")
            print(f"   Total Scenes: {result['metrics']['totalScenes']}")
            return True
        else:
            print(f"   ❌ Quality calculation missing required fields")
            return False
            
    except Exception as e:
        print(f"❌ Quality calculator test failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🚀 Starting Railway PDF Service Tests\n")
    
    tests = [
        test_health_endpoint,
        test_import_dependencies,
        test_pattern_recognition,
        test_quality_calculator
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Railway PDF service is ready.")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)