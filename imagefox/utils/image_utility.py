"""
image_utility.py
----------------

Utility module for image operations such as compression, format conversion,
and EXIF metadata editing using Pillow and piexif.

Author: Pradyumna Das Roy
License: MIT
"""

import os
import piexif
from PIL import Image


def compress_image(input_path: str, output_path: str, quality: int = 75, resize: str = None) -> None:
    """
    Compress an image by reducing its quality and optionally resizing.

    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the compressed image.
        quality (int): Compression quality (1-100). Higher means better quality.
        resize (str): Optional resize in format 'WIDTHxHEIGHT' (e.g., '800x600').

    Raises:
        IOError: If image cannot be opened or saved.
    """
    print(f"[INFO] Compressing image: {input_path}")
    try:
        img = Image.open(input_path)
        if resize:
            width, height = map(int, resize.lower().split('x'))
            print(f"[INFO] Resizing image to {width}x{height}")
            img = img.resize((width, height), Image.LANCZOS)

        img.save(output_path, quality=quality, optimize=True)
        print(f"[SUCCESS] Image compressed and saved to: {output_path}")
    except Exception as e:
        print(f"[ERROR] Failed to compress image: {e}")
        raise


def convert_image(input_path: str, output_path: str, format: str) -> None:
    """
    Convert an image to a different format.

    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the converted image.
        format (str): Format to convert to (e.g., 'jpeg', 'png').

    Raises:
        IOError: If image cannot be opened or saved.
    """
    print(f"[INFO] Converting image: {input_path} -> {format.upper()}")
    try:
        img = Image.open(input_path)
        img.save(output_path, format=format.upper())
        print(f"[SUCCESS] Image saved as {format.upper()} at {output_path}")
    except Exception as e:
        print(f"[ERROR] Failed to convert image: {e}")
        raise


def read_metadata(input_path: str) -> dict:
    """
    Read EXIF metadata from an image.

    Args:
        input_path (str): Path to the image file.

    Returns:
        dict: Parsed EXIF data as a dictionary.

    Raises:
        IOError: If EXIF data cannot be read.
    """
    print(f"[INFO] Reading metadata from: {input_path}")
    try:
        exif_dict = piexif.load(input_path)
        print(f"[INFO] Metadata keys found: {list(exif_dict.keys())}")
        return exif_dict
    except Exception as e:
        print(f"[ERROR] Failed to read metadata: {e}")
        raise


def remove_metadata(input_path: str, output_path: str) -> None:
    """
    Remove all EXIF metadata from an image.

    Args:
        input_path (str): Path to the original image.
        output_path (str): Path to save the cleaned image.

    Raises:
        IOError: If image cannot be saved or stripped.
    """
    print(f"[INFO] Removing metadata from: {input_path}")
    try:
        img = Image.open(input_path)
        data = list(img.getdata())
        img_no_exif = Image.new(img.mode, img.size)
        img_no_exif.putdata(data)
        img_no_exif.save(output_path)
        print(f"[SUCCESS] Metadata removed. Clean image saved at: {output_path}")
    except Exception as e:
        print(f"[ERROR] Failed to remove metadata: {e}")
        raise


def edit_metadata(input_path: str, output_path: str, field: str, value: str) -> None:
    """
    Edit a specific EXIF field in an image.

    Args:
        input_path (str): Path to the original image.
        output_path (str): Path to save the updated image.
        field (str): EXIF tag (e.g., 'Model', 'DateTime').
        value (str): New value to set for the tag.

    Raises:
        ValueError: If tag is invalid.
        IOError: If the image can't be modified or saved.
    """
    print(f"[INFO] Editing metadata field '{field}' to value '{value}' in: {input_path}")
    try:
        exif_dict = piexif.load(input_path)
        tag_bytes = value.encode('utf-8')

        if field == "Model":
            exif_dict["0th"][piexif.ImageIFD.Model] = tag_bytes
        elif field == "DateTime":
            exif_dict["0th"][piexif.ImageIFD.DateTime] = tag_bytes
        else:
            raise ValueError(f"Unsupported EXIF field: {field}")

        exif_bytes = piexif.dump(exif_dict)
        img = Image.open(input_path)
        img.save(output_path, exif=exif_bytes)
        print(f"[SUCCESS] Metadata field '{field}' updated and saved to: {output_path}")
    except Exception as e:
        print(f"[ERROR] Failed to edit metadata: {e}")
        raise
