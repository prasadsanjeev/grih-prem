#!/usr/bin/env python3
"""
Fix broken links in HTML files by converting index.html%3Fp=... to proper paths
and ensuring all relative paths are correct.
"""

import os
import re
from pathlib import Path
from urllib.parse import unquote

# Mapping of post IDs to proper page paths
POST_ID_MAP = {
    '5733': 'buy/',
    '5835': 'sell/',
    '140': 'blog/',
    '4827': 'faqs/',
    '142': 'contact/',
    '3': 'about-us/',
    '4574': 'agency/',
    '4577': 'agent/',
    '48': 'property-type/',
    '51': 'category/',
    '54': 'author/',
    '57': 'comments/',
    '5254': '',  # Home page
}

def fix_links_in_html(file_path, depth):
    """Fix broken links in an HTML file based on directory depth."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Calculate the relative path prefix needed
    prefix = '../' * depth
    
    # Fix index.html%3Fp=... patterns to clean paths
    # Pattern: index.html%3Fp=5733 or index.html?p=5733
    pattern = r'index\.html[%?]3?[Fp]=(\d+)(\.html)?'
    
    def replace_post_link(match):
        post_id = match.group(1)
        if post_id in POST_ID_MAP:
            target_path = POST_ID_MAP[post_id]
            if target_path:
                return f'{prefix}{target_path}'
            else:
                return f'{prefix}index.html'
        return match.group(0)
    
    content = re.sub(pattern, replace_post_link, content)
    
    # Fix feed links
    content = re.sub(
        r'(?<!%3D)feed/(?!index\.html)',
        f'{prefix}feed/index.html',
        content
    )
    content = re.sub(
        r'\.\.(?:/\.\.)+/feed/',
        f'{prefix}feed/',
        content
    )
    
    # Fix comments feed links
    content = re.sub(
        r'comments/feed/(?!index\.html)',
        f'{prefix}comments/feed/index.html',
        content
    )
    
    # Fix wp-json paths
    content = re.sub(
        r'(?<!")\.\.(?:/\.\.)+/wp-json/',
        f'{prefix}wp-json/',
        content
    )
    content = re.sub(
        r'(?<!")/wp-json/',
        f'{prefix}wp-json/',
        content
    )
    
    # Fix wp-content paths
    content = re.sub(
        r'(?<!")\.\.(?:/\.\.)+/wp-content/',
        f'{prefix}wp-content/',
        content
    )
    
    # Fix wp-includes paths
    content = re.sub(
        r'(?<!")\.\.(?:/\.\.)+/wp-includes/',
        f'{prefix}wp-includes/',
        content
    )
    
    # Only write if content changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def get_directory_depth(file_path, root_path):
    """Calculate the depth of a file relative to the root."""
    rel_path = os.path.relpath(file_path, root_path)
    # Count how many directories deep this file is
    depth = rel_path.count(os.sep)
    return depth

def process_html_files(root_path):
    """Process all HTML files in the directory tree."""
    fixed_count = 0
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Skip certain directories
        skip_dirs = ['.git', 'wp-content', 'wp-includes', '.git']
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        
        for filename in filenames:
            if filename.endswith('.html'):
                file_path = os.path.join(dirpath, filename)
                depth = get_directory_depth(file_path, root_path)
                
                # Files in root are depth 0, files in subdirs have higher depth
                if depth > 0:
                    depth -= 1  # Adjust for file itself
                
                print(f"Processing: {file_path} (depth: {depth})")
                if fix_links_in_html(file_path, depth):
                    fixed_count += 1
                    print(f"  ✓ Fixed links in {filename}")
                else:
                    print(f"  - No changes needed in {filename}")
    
    return fixed_count

if __name__ == '__main__':
    root_path = os.path.dirname(os.path.abspath(__file__))
    print(f"Starting link fixes in: {root_path}\n")
    
    fixed = process_html_files(root_path)
    print(f"\n✓ Fixed links in {fixed} files")
