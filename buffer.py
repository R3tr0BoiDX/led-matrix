from typing import List

import colors
import settings
from pixel import Pixel
from debug import DebugDisplay

# todo: think about if this is really needed

# Only needed to initialize buffers and display
_WIDTH = settings.get_display_width()
_HEIGHT = settings.get_display_height()

DEBUG_MODE = settings.get_debug()
if DEBUG_MODE:
    _DISPLAY = DebugDisplay(_WIDTH, _HEIGHT)
else:
    # todo: implement hardware.py
    # from hardware import Display
    # display = Display()
    pass


def get_new_buffer(width: int, height: int) -> List[List[Pixel]]:
    # Create a new buffer with the given dimensions
    return [
        [Pixel(colors.BACKGROUND_COLOR) for _ in range(width)] for _ in range(height)
    ]


def _clear_buffer(buffer: List[List[Pixel]]):
    # Clear a given buffer
    for y, row in enumerate(buffer):
        for x, _ in enumerate(row):
            buffer[y][x] = Pixel(colors.BACKGROUND_COLOR)


def display_buffer():
    BUFFER_MANAGER.swap_buffers()
    BUFFER_MANAGER.clear_back_buffer()
    BUFFER_MANAGER.display()


def shutdown():
    _DISPLAY.shutdown()


class BufferManager:
    def __init__(self, width, height):
        self.front_buffer = get_new_buffer(width, height)
        self.back_buffer = get_new_buffer(width, height)

    def clear_back_buffer(self):
        _clear_buffer(self.back_buffer)

    def write_to_buffer(self, data: List[List[Pixel]]):
        for y, row in enumerate(data):
            for x, pixel in enumerate(row):
                if pixel.color != colors.TRANSPARENT_COLOR:
                    self.back_buffer[y][x] = pixel

    def swap_buffers(self):
        self.front_buffer, self.back_buffer = self.back_buffer, self.front_buffer

    def display(self):
        _DISPLAY.clear()
        _DISPLAY.update(self.front_buffer)
        _DISPLAY.display()


BUFFER_MANAGER = BufferManager(_WIDTH, _HEIGHT)
