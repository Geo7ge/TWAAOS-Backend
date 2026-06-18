#!/usr/bin/env python3
"""
Script to build Sphinx documentation automatically.
"""

import os
import sys
import subprocess
from pathlib import Path

def build_docs():
    """Build the Sphinx documentation."""
    # Set dummy environment variables for documentation
    os.environ.setdefault('SECRET_KEY', 'dummy_secret_key_for_docs')
    os.environ.setdefault('SUPABASE_URL', 'dummy_url')
    os.environ.setdefault('SUPABASE_KEY', 'dummy_key')
    os.environ.setdefault('SUPABASE_SERVICE_KEY', 'dummy_service_key')

    # Get the directory of this script
    script_dir = Path(__file__).parent
    docs_dir = script_dir / 'docs'

    # Change to docs directory
    os.chdir(docs_dir)

    # Build HTML documentation
    cmd = [sys.executable, '-m', 'sphinx', '-b', 'html', '.', '_build/html']
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("Documentation built successfully!")
        print(f"HTML files are in: {docs_dir / '_build' / 'html'}")
        print(f"Open {docs_dir / '_build' / 'html' / 'index.html'} in your browser")
        print("\nAlternative manual commands:")
        print(f"  cd {docs_dir}")
        print("  python -m sphinx -b html . _build/html")
        print("  # or")
        print("  sphinx-build -b html . _build/html  (if sphinx-build is in PATH)")
    else:
        print("Error building documentation:")
        print(result.stderr)
        sys.exit(1)

if __name__ == '__main__':
    build_docs()