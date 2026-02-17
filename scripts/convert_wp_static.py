#!/usr/bin/env python3
import os
import re

ROOT = '/Users/sanjeev/Documents/grih.ca'

count_files = 0
count_changes = 0

domain_pattern = re.compile(r'https?://(?:www\.)?grih\.ca', re.IGNORECASE)
xmlrpc_pattern = re.compile(r'href=["\'][^"\']*xmlrpc\.php[^"\']*["\']', re.IGNORECASE)
form_admin_ajax_pattern = re.compile(r'(<form\b[^>]*?\baction=["\'])([^"\']*admin-ajax\.php)(["\'])([^>]*>)', re.IGNORECASE | re.DOTALL)
var_ajaxurl_pattern = re.compile(r'(var\s+ajaxurl\s*=\s*["\'])(https?://(?:www\.)?grih\.ca/)?(wp-admin/admin-ajax\.php)(["\'])', re.IGNORECASE)
json_ajaxurl_pattern = re.compile(r'(["\']ajaxurl["\']\s*:\s*["\'])(https?://(?:www\.)?grih\.ca/)?(wp-admin/admin-ajax\.php)(["\'])', re.IGNORECASE)

def process_file(path):
    global count_changes
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()

    orig = s

    # Replace domain occurrences with relative paths (remove the domain)
    s = domain_pattern.sub('', s)

    # Neutralize xmlrpc links
    s = xmlrpc_pattern.sub('href="#"', s)

    # Neutralize form actions that post to admin-ajax.php and add data-original-action attr
    def form_repl(m):
        prefix = m.group(1)
        orig_action = m.group(2)
        quote = m.group(3)
        rest = m.group(4)
        # Insert data-original-action after the action attribute
        return f"{prefix}#{quote} data-original-action=\"{orig_action}\"{rest}"

    s = form_admin_ajax_pattern.sub(form_repl, s)

    # Replace JS var ajaxurl definitions to '#' to avoid AJAX calls
    s = var_ajaxurl_pattern.sub(r"\1#\4", s)
    s = json_ajaxurl_pattern.sub(r"\1#\4", s)

    if s != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(s)
        count_changes += 1
        print(f"Patched: {path}")


for dirpath, dirnames, filenames in os.walk(ROOT):
    for fn in filenames:
        if fn.lower().endswith('.html'):
            count_files += 1
            process_file(os.path.join(dirpath, fn))

print(f"Scanned {count_files} HTML files, modified {count_changes} files.")
