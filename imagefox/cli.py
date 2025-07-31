"""
cli.py
------

Entry point for the imagefox command-line interface.
Handles argument parsing and dispatches to specific operations like compress, convert, and metadata edit.

Author: Pradyumna Das Roy
License: MIT
"""

import argparse
import json
from imagefox.utils.image_utility import (
    compress_image,
    convert_image,
    read_metadata,
    remove_metadata,
    edit_metadata,
    apply_metadata_from_json
)


def main():
    parser = argparse.ArgumentParser(
        prog="imagefox",
        description="🦊 ImageFox - CLI toolkit for image compression, conversion, and metadata editing."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Sub-command: compress
    compress_parser = subparsers.add_parser("compress", help="Compress an image")
    compress_parser.add_argument("input", help="Path to input image")
    compress_parser.add_argument("--output", required=True, help="Path to output image")
    compress_parser.add_argument("--quality", type=int, default=75, help="Compression quality (1–100)")
    compress_parser.add_argument("--resize", help="Resize in format WIDTHxHEIGHT (e.g., 800x600)")

    # Sub-command: convert
    convert_parser = subparsers.add_parser("convert", help="Convert image format")
    convert_parser.add_argument("input", help="Path to input image")
    convert_parser.add_argument("--output", required=True, help="Path to output image")
    convert_parser.add_argument("--to", required=True, help="Format to convert to (e.g., jpeg, png)")

    # Sub-command: metadata view
    meta_view_parser = subparsers.add_parser("metadata-view", help="View EXIF metadata")
    meta_view_parser.add_argument("input", help="Path to input image")

    # Sub-command: metadata remove
    meta_remove_parser = subparsers.add_parser("metadata-remove", help="Remove all metadata")
    meta_remove_parser.add_argument("input", help="Path to input image")
    meta_remove_parser.add_argument("--output", required=True, help="Path to save cleaned image")

    # Sub-command: metadata edit
    meta_edit_parser = subparsers.add_parser("metadata-edit", help="Edit specific EXIF metadata field")
    meta_edit_parser.add_argument("input", help="Path to input image")
    meta_edit_parser.add_argument("--output", required=True, help="Path to save updated image")
    meta_edit_parser.add_argument("--field", required=True, help="EXIF field to edit (e.g., Model)")
    meta_edit_parser.add_argument("--value", required=True, help="New value for the EXIF field")

    # Sub-command: metadata write from JSON
    meta_write_parser = subparsers.add_parser("metadata-write", help="Apply full EXIF metadata from a JSON file")
    meta_write_parser.add_argument("input", help="Path to input image (JPEG)")
    meta_write_parser.add_argument("--json", required=True, help="Path to JSON file containing metadata")

    args = parser.parse_args()

    # Dispatch to appropriate handler
    if args.command == "compress":
        compress_image(args.input, args.output, args.quality, args.resize)

    elif args.command == "convert":
        convert_image(args.input, args.output, args.to)

    elif args.command == "metadata-view":
        metadata = read_metadata(args.input)
        print("[INFO] EXIF Metadata:")
        for ifd, data in metadata.items():
            print(f"{ifd}:")
            for tag, val in data.items():
                print(f"  {tag}: {val}")

    elif args.command == "metadata-remove":
        remove_metadata(args.input, args.output)

    elif args.command == "metadata-edit":
        edit_metadata(args.input, args.output, args.field, args.value)

    elif args.command == "metadata-write":
        try:
            with open(args.json, "r", encoding="utf-8") as f:
                meta_data = json.load(f)
            apply_metadata_from_json(args.input, meta_data)
        except Exception as e:
            print(f"[ERROR] Failed to load metadata JSON: {e}")
            raise


if __name__ == "__main__":
    main()
