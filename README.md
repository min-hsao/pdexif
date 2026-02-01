# pdexif - Preview & Describe EXIF

A lightweight CLI tool to preview images/videos and interactively add EXIF descriptions using ExifTool.

## Features

- 👁️ Preview files with your system's default viewer
- ✏️ Add or update EXIF metadata fields
- 🔄 Skip files that already have descriptions
- 📁 Batch process entire directories
- 🎯 Filter by file type

## Requirements

- Python 3.6+
- ExifTool (`brew install exiftool` on macOS)

## Installation

```bash
# Install ExifTool (macOS)
brew install exiftool
```

## Usage

```bash
# Process current directory
python pdexif.py

# Specify directory
python pdexif.py /path/to/files

# Update Title field instead of Description
python pdexif.py --field Title

# Only process JPG and PNG
python pdexif.py --types jpg,png

# Overwrite existing descriptions
python pdexif.py --overwrite

# Debug mode
python pdexif.py --debug
```

## Arguments

| Argument | Description |
|----------|-------------|
| `directory` | Directory to scan (default: current) |
| `--field` | EXIF field to update (default: Description) |
| `--types` | Comma-separated extensions (default: jpg,jpeg,png,mp4,mov,avi) |
| `--overwrite` | Edit files even if they have descriptions |
| `--debug` | Enable debug output |

## Workflow

1. Script opens each file for preview
2. You enter a description (or press Enter to skip)
3. Description is saved to EXIF metadata
4. Repeat for all files

## License

MIT License - see [LICENSE](LICENSE) for details.
