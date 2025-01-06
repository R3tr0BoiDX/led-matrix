import platform
from typing import List

from src import colors, log, settings
from src.pixel import Pixel

# Only needed to initialize buffers and display
_width = settings.Display().get_width()
_height = settings.Display().get_height()

logger = log.get_logger(__name__)

if platform.machine() == "x86_64":
    logger.info("Detected x86_64 platform, creating debug display")
    from src.display.debug import DebugDisplay

    _display = DebugDisplay(_width, _height)

elif platform.machine() == "armv6l":
    logger.info("Detected armv6l platform, creating LED display")
    from src.display.led import LedDisplay

    _display = LedDisplay((_width, _height))

else:
    raise NotImplementedError("Unsupported platform")


def get_new_buffer(width: int, height: int) -> List[List[Pixel]]:
    # Create a new buffer with the given dimensions
    logger.debug("Creating new buffer with dimensions: %d x %d", width, height)
    return [
        [Pixel(colors.BACKGROUND_COLOR) for _ in range(width)] for _ in range(height)
    ]


# Can't be defined further up because it depends on _width, _height and get_new_buffer() :(
_final_buffer = get_new_buffer(_width, _height)


def clear_buffer():
    _clear_a_buffer(_final_buffer)


def copy_buffers(
    work_buffer: List[List[Pixel]],
    display_buffer: List[List[Pixel]],
):
    # Swap the buffers
    logger.debug("Copying work buffer to display buffer")
    for y, row in enumerate(display_buffer):
        for x, _ in enumerate(row):
            display_buffer[y][x] = work_buffer[y][x]


def _clear_a_buffer(buffer: List[List[Pixel]]):
    # Clear a given buffer
    logger.debug("Clearing buffer")
    for y, row in enumerate(buffer):
        for x, _ in enumerate(row):
            buffer[y][x] = Pixel(colors.BACKGROUND_COLOR)


def write_to_buffer(data: List[List[Pixel]]):
    # Write data to the buffer
    logger.debug("Writing data to buffer")
    for y, row in enumerate(data):
        for x, pixel in enumerate(row):
            if pixel.color != colors.TRANSPARENT_COLOR:
                _final_buffer[y][x] = pixel


def display():
    _display.clear()
    _display.update(_final_buffer)
    _display.display()


def shutdown():
    _display.shutdown()


def get_display():
    return _display
