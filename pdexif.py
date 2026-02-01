#!/usr/bin/env python3
"""
pdexif.py
by Min-Hsao Chen (w/ ChatGPT-4)
v0.0002 - 2024-06-04

Lightweight CLI tool to preview images/videos, prompt for a description,
and update EXIF metadata using ExifTool.

Usage:
    python3 pdexif.py [directory] [options]

Arguments:
    directory           Optional. Folder containing files. Defaults to current directory.

Options:
    --field FIELD       EXIF field to update (Description, Title, Comment, XPComment, etc.)
                        Default: Description
    --types EXT1,EXT2   Comma-separated list of file extensions to include (no dots).
                        Default: jpg,jpeg,png,mp4,mov,avi
    --overwrite         Edit even if the file already has a description (default: skip such files)
    -h, --help          Show this help message and exit.

Examples:
    python3 pdexif.py
    python3 pdexif.py /path/to/files --field Title --types jpg,png
    python3 pdexif.py --overwrite

Requires:
    exiftool (install via 'brew install exiftool' if on Mac)
"""

import os
import sys
import subprocess

def print_help():
    print(__doc__)

def get_existing_description(filepath, field):
    # Query exiftool for the current value of the field
    cmd = ['exiftool', f'-{field}', '-s', '-s', '-s', filepath]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Preview files and add EXIF descriptions via exiftool.",
        add_help=False
    )
    parser.add_argument('directory', nargs='?', default=os.getcwd(),
                        help='Directory to scan for files (default: current dir)')
    parser.add_argument('--field', default='Description',
                        help='EXIF field to update (default: Description)')
    parser.add_argument('--types', default='jpg,jpeg,png,mp4,mov,avi',
                        help='Comma-separated list of file extensions (default: jpg,jpeg,png,mp4,mov,avi)')
    parser.add_argument('--overwrite', action='store_true',
                        help='Edit even if the file already has a description')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug output')
    parser.add_argument('-h', '--help', action='help', help='Show this help message and exit')
    args = parser.parse_args()

    folder = args.directory
    exif_field = args.field
    extensions = tuple(f'.{e.lower()}' for e in args.types.split(','))
    overwrite = args.overwrite
    debug = args.debug

    if debug:
        print(f"[DEBUG] Script started")
        print(f"[DEBUG] folder={folder}")
        print(f"[DEBUG] exif_field={exif_field}")
        print(f"[DEBUG] extensions={extensions}")
        print(f"[DEBUG] overwrite={overwrite}")

    if not os.path.isdir(folder):
        print(f"Error: '{folder}' is not a directory.")
        sys.exit(1)

    try:
        all_files = sorted(os.listdir(folder))
    except Exception as e:
        print(f"Error reading directory '{folder}': {e}")
        sys.exit(1)

    files = [f for f in all_files if f.lower().endswith(extensions)]
    if debug:
        print(f"[DEBUG] all_files={all_files}")
        print(f"[DEBUG] matched files={files}")
    if not files:
        print(f"No supported files found in '{folder}'.")
        return

    print(f"\n--- Preview & Describe EXIF v0.0002 ---")
    print(f"Folder: {folder}")
    print(f"EXIF field: {exif_field}")
    print(f"File types: {', '.join(extensions)}")
    print(f"Skip files with description: {'No (will overwrite)' if overwrite else 'Yes'}\n")
    print("Press Enter without typing to skip a file.\n")

    for fname in files:
        fpath = os.path.join(folder, fname)

        # Check existing description
        if not overwrite:
            existing = get_existing_description(fpath, exif_field)
            if debug:
                print(f"[DEBUG] {fname} existing description: {existing}")
            if existing:
                print(f"\n{fname} already has a description, skipping.")
                print(f"    Existing description: {existing}")
                continue

        print(f"\nOpening: {fname}")
        subprocess.run(['open', fpath])

        try:
            desc = input("Enter description (leave empty to skip): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        if not desc:
            print("Skipped.")
            continue

        cmd = [
            'exiftool',
            f'-{exif_field}={desc}',
            '-overwrite_original',
            fpath
        ]
        if debug:
            print(f"[DEBUG] Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Updated {exif_field} for {fname}.")
        else:
            print(f"Error updating {fname}: {result.stderr}")

    print("\nAll done!")

if __name__ == "__main__":
    main()
