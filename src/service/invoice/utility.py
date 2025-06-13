import io
import os
import re
from pathlib import Path
from typing import Tuple

from PIL import Image


def get_secret_keys() -> dict:
    return {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_KEY"),
        "region_name": os.getenv("REGION_NAME"),
    }


def image_to_byte_string(image_path: str | Path) -> Tuple[bytes, str]:
    image = Image.open(image_path)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")  # or 'JPEG', etc.
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr, image.get_format_mimetype() or "image/png"


def sorted_images(image_dir: str | Path) -> list[Path]:
    """Returns a list of PNG files sorted by page number."""
    image_files = list(Path(image_dir).rglob("*.png"))

    # Regex to extract page number
    def extract_page_num(file: Path) -> int:
        match = re.search(r"Page_(\d+)\.png", file.name)
        return int(match.group(1)) if match else 1000000  # Handle non-matching files by placing them at the end

    return sorted(image_files, key=extract_page_num)
