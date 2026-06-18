#!/usr/bin/env python3
"""
Script to generate UML diagrams from PlantUML files.
"""

import os
import subprocess
import sys
from pathlib import Path

def generate_diagrams():
    """Generate PNG images from PlantUML files."""
    script_dir = Path(__file__).parent
    diagrams_dir = script_dir / 'diagrams'

    if not diagrams_dir.exists():
        print("Diagrams directory not found!")
        return

    # Find all .puml files
    puml_files = list(diagrams_dir.glob('*.puml'))

    if not puml_files:
        print("No .puml files found in diagrams directory!")
        return

    print(f"Found {len(puml_files)} PlantUML files")

    # Try to use plantuml command
    try:
        for puml_file in puml_files:
            print(f"Generating diagram for {puml_file.name}...")
            cmd = ['plantuml', str(puml_file)]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=diagrams_dir)

            if result.returncode == 0:
                print(f"✓ Generated {puml_file.stem}.png")
            else:
                print(f"✗ Failed to generate {puml_file.name}: {result.stderr}")

    except FileNotFoundError:
        print("plantuml command not found. Trying with python -m plantuml...")

        # Try with python module
        try:
            for puml_file in puml_files:
                print(f"Generating diagram for {puml_file.name}...")
                cmd = [sys.executable, '-m', 'plantuml', str(puml_file)]
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=diagrams_dir)

                if result.returncode == 0:
                    print(f"✓ Generated {puml_file.stem}.png")
                else:
                    print(f"✗ Failed to generate {puml_file.name}: {result.stderr}")

        except Exception as e:
            print(f"Error generating diagrams: {e}")
            print("\nTo generate diagrams manually:")
            print("1. Install PlantUML: pip install plantuml")
            print("2. Or download from: https://plantuml.com/download")
            print("3. Run: plantuml diagrams/*.puml")
            print("4. Or use online editor: https://www.plantuml.com/plantuml")

if __name__ == '__main__':
    generate_diagrams()