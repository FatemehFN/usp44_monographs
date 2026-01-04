#!/usr/bin/env python3
"""
Fix formulas and empty pre-filled input boxes in Farsi monograph HTML files.
"""

import re
import glob
import os

def fix_html_file(file_path):
    """Fix formulas and empty input boxes in a single HTML file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes = []
    
    # Fix broken LaTeX formulas
    # 1. Fix \frac written as rac
    if 'rac{' in content:
        content = re.sub(r'(?<!\\f)rac\{', r'\\frac{', content)
        changes.append("Fixed \\frac syntax")
    
    # 2. Remove value attributes from ALL input fields (including readonly ones)
    # Pattern: value="..." in input tags
    pattern = r'<input[^>]*value="[^"]*"[^>]*>'
    matches = list(re.finditer(pattern, content))
    
    for match in matches:
        full_tag = match.group(0)
        # Remove the value attribute
        new_tag = re.sub(r'\s+value="[^"]*"', '', full_tag)
        content = content.replace(full_tag, new_tag)
        if "Removed value attribute" not in changes:
            changes.append("Removed value attributes from all input fields")
    
    # Check if any changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes
    
    return False, []

def main():
    # Get all Farsi monograph HTML files
    html_files = glob.glob('/Users/fsfatemi/Pharmacopeia/usp44_monographs/*_farsi.html')
    
    print(f"Found {len(html_files)} Farsi monograph files\n")
    
    modified_count = 0
    
    for file_path in sorted(html_files):
        file_name = os.path.basename(file_path)
        modified, changes = fix_html_file(file_path)
        
        if modified:
            modified_count += 1
            print(f"✓ {file_name}")
            for change in changes:
                print(f"  - {change}")
        else:
            print(f"○ {file_name} (no changes needed)")
    
    print(f"\n{'='*60}")
    print(f"Modified {modified_count} out of {len(html_files)} files")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
