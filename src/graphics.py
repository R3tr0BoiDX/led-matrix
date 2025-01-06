from pathlib import Path
from typing import List, Tuple

from PIL import Image

from src import colors, log, settings
from src.pixel import Pixel

RESOURCES = settings.Resources().get_path()
FILE_EXTENSION_PNG = ".png"

logger = log.get_logger(__name__)


def get_filepath(filename, file_extension=FILE_EXTENSION_PNG) -> Path:
    path = Path(f"./{RESOURCES}/{filename}{file_extension}")
    logger.debug("Resource filepath: %s", path)
    return path


def read_image(image_path: Path) -> List[List[Pixel]]:
    # Load the image
    try:
        image = Image.open(image_path).convert("RGB")
    except FileNotFoundError as e:
        logger.error("File not found: %s", e)
        return read_image(get_filepath("invalid"))

    # Get image dimensions
    width, height = image.size
    logger.debug("Image dimensions: %s x %s", width, height)

    # Create a 2D list to hold pixel color values
    pixel_data = []

    # Populate the 2D list with pixel color values
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b = image.getpixel((x, y))  # Get the pixel's RGB value
            row.append(Pixel((r, g, b)))  # Append the RGB tuple to the current row
        pixel_data.append(row)  # Append the row to the pixel data
    logger.debug("Pixel data: %s", pixel_data)

    return pixel_data  # Return the 2D list of pixel colors


def draw_graphic(
    pixels: List[List[Pixel]],
    data: List[List[Pixel]],
    offset: Tuple[int, int],
    color_override: Tuple[int, int, int] = None,
) -> None:
    x_offset, y_offset = offset
    logger.debug("Drawing graphic at offset: %s, %s", x_offset, y_offset)

    # Enumerate through the graphic data
    for y, row in enumerate(data):
        for x, pixel in enumerate(row):

            # Check if the pixel is within the bounds of the display
            if y + y_offset < len(pixels) and x + x_offset < len(pixels[0]):

                # Draw the pixel if it's not transparent
                if pixel.color != colors.TRANSPARENT_COLOR:

                    # Override the color if wanted
                    if color_override:
                        pixel.color = color_override

                    # Draw the pixel
                    pixels[y + y_offset][x + x_offset] = pixel
