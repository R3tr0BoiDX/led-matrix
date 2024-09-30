from pathlib import Path
from typing import List

from PIL import Image

from pixel import Pixel

RESOURCES = "res"
FILE_EXTENSION_PNG = ".png"
FILE_EXTENSION_GIF = ".gif"


def get_filepath(filename, file_extension=FILE_EXTENSION_PNG) -> Path:
    return Path(f"./{RESOURCES}/{filename}{file_extension}")


def read_image(image_path: Path) -> List[List[Pixel]]:
    # Load the image
    try:
        image = Image.open(image_path).convert("RGB")
    except FileNotFoundError:
        print(f"File not found: {image_path}")
        return read_image(get_filepath("invalid"))

    # Get image dimensions
    width, height = image.size

    # Create a 2D list to hold pixel color values
    pixel_data = []

    # Populate the 2D list with pixel color values
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b = image.getpixel((x, y))  # Get the pixel's RGB value
            row.append(Pixel((r, g, b)))  # Append the RGB tuple to the current row
        pixel_data.append(row)  # Append the row to the pixel data

    return pixel_data  # Return the 2D list of pixel colors
