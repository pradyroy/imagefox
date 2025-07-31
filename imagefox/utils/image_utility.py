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
from fractions import Fraction


def compress_image(
    input_path: str, output_path: str, quality: int = 75, resize: str = None
) -> None:
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
            width, height = map(int, resize.lower().split("x"))
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
    Read and parse EXIF metadata from an image, formatting tag IDs to human-readable names.

    Args:
        input_path (str): Path to the input image.

    Returns:
        dict: Dictionary with EXIF sections and their human-readable tag-value pairs.

    Raises:
        IOError: If the image or EXIF data cannot be read.
    """
    print(f"[INFO] Reading metadata from: {input_path}")
    try:
        exif_dict = piexif.load(input_path)
        print(f"[INFO] Metadata keys found: {list(exif_dict.keys())}")

        readable_metadata = {}

        for section, tags in exif_dict.items():
            if isinstance(tags, dict):
                readable_section = {}
                for tag_id, value in tags.items():
                    tag_name = (
                        piexif.TAGS.get(section, {})
                        .get(tag_id, {})
                        .get("name", f"Tag-{tag_id}")
                    )
                    readable_section[tag_name] = value
                readable_metadata[section] = readable_section
            else:
                print(f"[INFO] Skipping non-dictionary section: {section}")

        return readable_metadata

    except Exception as e:
        print(f"[ERROR] Failed to read metadata: {e}")
        raise IOError(f"Could not read EXIF metadata from {input_path}") from e


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
    print(
        f"[INFO] Editing metadata field '{field}' to value '{value}' in: {input_path}"
    )
    try:
        exif_dict = piexif.load(input_path)
        tag_bytes = value.encode("utf-8")

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


def _deg_to_dms_rational(deg_float):
    """
    Convert decimal degrees to EXIF-compatible DMS format with rational numbers.
    """
    deg = int(deg_float)
    min_float = (deg_float - deg) * 60
    minute = int(min_float)
    sec_float = (min_float - minute) * 60
    sec = Fraction(round(sec_float, 4)).limit_denominator(10000)
    return [(deg, 1), (minute, 1), (sec.numerator, sec.denominator)]


def apply_metadata_from_json(image_path: str, metadata_json: dict) -> None:
    """
    Apply EXIF metadata to a JPEG image using a structured JSON input.

    Args:
        image_path (str): Path to the JPEG image to update (in-place).
        metadata_json (dict): Dictionary containing "0th", "Exif", and optional GPS ("Latitude", "Longitude").

    Raises:
        IOError: If the image cannot be opened or metadata cannot be applied.
    """
    print(f"[INFO] Applying metadata to: {image_path}")
    try:
        # Initialize empty EXIF dictionary
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "Interop": {}}

        # Handle 0th and Exif tags using piexif.TAGS
        for ifd in ["0th", "Exif"]:
            for key, val in metadata_json.get(ifd, {}).items():
                for tag_id, tag_info in piexif.TAGS[ifd].items():
                    if tag_info["name"] == key:
                        if isinstance(val, str):
                            val = val.encode("utf-8")
                        exif_dict[ifd][tag_id] = val
                        break

        # Handle optional GPS conversion from decimal
        gps = metadata_json.get("GPS", {})
        if "Latitude" in gps and "Longitude" in gps:
            lat = gps["Latitude"]
            lng = gps["Longitude"]
            exif_dict["GPS"][piexif.GPSIFD.GPSLatitudeRef] = b"N" if lat >= 0 else b"S"
            exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = _deg_to_dms_rational(abs(lat))
            exif_dict["GPS"][piexif.GPSIFD.GPSLongitudeRef] = b"E" if lng >= 0 else b"W"
            exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = _deg_to_dms_rational(
                abs(lng)
            )

        # Dump EXIF and save to image
        exif_bytes = piexif.dump(exif_dict)
        img = Image.open(image_path)
        img.save(image_path, exif=exif_bytes)
        print(f"[SUCCESS] Metadata applied successfully to: {image_path}")

    except Exception as e:
        print(f"[ERROR] Failed to apply metadata: {e}")
        raise IOError(f"Could not apply metadata to {image_path}") from e
