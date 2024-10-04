from typing import List
import platform

import colors
import settings
from pixel import Pixel

# Only needed to initialize buffers and display
_width = settings.get_display_width()
_height = settings.get_display_height()

if platform.machine() == "x86_64":
    from display.debug import DebugDisplay
    _display = DebugDisplay(_width, _height)
elif platform.machine() == "armv6l":
    from display.led import LedDisplay
    _display = LedDisplay((_width, _height))
else:
    raise NotImplementedError("Unsupported platform")


def get_new_buffer(width: int, height: int) -> List[List[Pixel]]:
    # Create a new buffer with the given dimensions
    return [
        [Pixel(colors.BACKGROUND_COLOR) for _ in range(width)] for _ in range(height)
    ]


# Cant be defined further up because it depends on _width, _height and get_new_buffer() :(
_buffer = get_new_buffer(_width, _height)


def clear_buffer():
    _clear_a_buffer(_buffer)


def copy_buffers(
    work_buffer: List[List[Pixel]],
    display_buffer: List[List[Pixel]],
):
    # Swap the buffers
    for y, row in enumerate(display_buffer):
        for x, _ in enumerate(row):
            display_buffer[y][x] = work_buffer[y][x]


def _clear_a_buffer(buffer: List[List[Pixel]]):
    # Clear a given buffer
    for y, row in enumerate(buffer):
        for x, _ in enumerate(row):
            buffer[y][x] = Pixel(colors.BACKGROUND_COLOR)


def write_to_buffer(data: List[List[Pixel]]):
    for y, row in enumerate(data):
        for x, pixel in enumerate(row):
            if pixel.color != colors.TRANSPARENT_COLOR:
                _buffer[y][x] = pixel


def display():
    _display.clear()
    _display.update(_buffer)
    _display.display()


def shutdown():
    _display.shutdown()
