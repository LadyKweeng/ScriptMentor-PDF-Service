#!/usr/bin/env python3
"""
Test the parser with the actual PDF file
"""

import sys
sys.path.append('/workspaces/ScriptMentor_Bolt_Dev/railway-pdf-service')

from screenplay_parser import ScreenplayParser
import json

def test_real_pdf():
    """Test with the actual TEST_PDF.pdf"""
    print("Testing with actual TEST_PDF.pdf...\n")

    parser = ScreenplayParser()

    try:
        # Parse the PDF
        result = parser.parse_pdf('/workspaces/ScriptMentor_Bolt_Dev/TEST_PDF.pdf')

        print(f"✅ PDF parsed successfully!")
        print(f"   Total scenes: {len(result['scenes'])}")
        print(f"   Total characters: {len(result['characters'])}")
        print(f"   Total pages: {result['totalPages']}")

        # Show first scene content (first 500 characters)
        if result['scenes']:
            first_scene = result['scenes'][0]
            content = first_scene.get('content', '')
            print(f"\nFirst scene content preview:")
            print("-" * 40)
            print(content[:500] + "..." if len(content) > 500 else content)
            print("-" * 40)

            # Check for key issues mentioned in Action_Spacing_Error.md
            print("\nChecking for specific issues:")

            # Check if "Discord circle jerk" appears as dialogue (good)
            if 'Discord circle jerk' in content:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'Discord circle jerk' in line:
                        leading_spaces = len(line) - len(line.lstrip())
                        if leading_spaces == 25:  # Dialogue indent
                            print(f"✅ 'Discord circle jerk' correctly formatted as dialogue (25 spaces)")
                        else:
                            print(f"❌ 'Discord circle jerk' incorrectly formatted ({leading_spaces} spaces)")
                        break

            # Check for HANNAH (CONT'D) patterns
            contd_found = False
            for line in content.split('\n'):
                if 'HANNAH' in line and 'CONT' in line:
                    leading_spaces = len(line) - len(line.lstrip())
                    if leading_spaces == 38:  # Character indent
                        print(f"✅ Character continuation correctly formatted: '{line.strip()}'")
                    else:
                        print(f"❌ Character continuation incorrectly formatted: '{line.strip()}' ({leading_spaces} spaces)")
                    contd_found = True
                    break

            if not contd_found:
                print("ℹ️  No HANNAH (CONT'D) patterns found in first scene")

        # Save full output for analysis
        with open('/workspaces/ScriptMentor_Bolt_Dev/railway-pdf-service/parsed_output.json', 'w') as f:
            json.dump(result, f, indent=2)

        print(f"\n✅ Full output saved to parsed_output.json")

        return result

    except Exception as e:
        print(f"❌ Error parsing PDF: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_real_pdf()
