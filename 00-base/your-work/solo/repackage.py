#!/usr/bin/env python3
"""Repackage intern-gds archive, excluding virtualenvs, caches, and large files."""
import os
import zipfile
import fnmatch
from pathlib import Path

BASE = Path('/Users/adrikamandal/Desktop/GEN AI/PrajnaAI/intern-gds')
OUTPUT = BASE / 'intern-gds-clean.zip'

# Patterns to exclude
EXCLUDE = [
    '*/venv',
    '*/venv-gds-owl',
    '*/__pycache__',
    '*/.pytest_cache',
    '*/__MACOSX',
    '*/.DS_Store',
    '*/chebi.owl',
    '*/export_rdf.py',
    '*/shapes.ttl',
    '*/shacl_report.md',
    '*.pyc',
]

def should_exclude(path):
    for pattern in EXCLUDE:
        if fnmatch.fnmatch(str(path), pattern):
            return True
    # Also exclude by name
    parts = Path(path).parts
    for part in parts:
        if part in ('venv', 'venv-gds-owl', '__pycache__', '.pytest_cache', '__MACOSX'):
            return True
        if part.endswith('.pyc') or part == '.DS_Store':
            return True
    return False

with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(BASE):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('venv', 'venv-gds-owl', '__pycache__', '.pytest_cache', '__MACOSX')]
        
        for file in files:
            if file == '.DS_Store' or file.endswith('.pyc'):
                continue
            filepath = Path(root) / file
            arcname = filepath.relative_to(BASE)
            
            if should_exclude(arcname):
                continue
            
            zf.write(filepath, arcname)
            print(f"Added: {arcname}")

print(f"\nArchive created: {OUTPUT}")
print(f"Size: {OUTPUT.stat().st_size / 1024 / 1024:.1f} MB")
