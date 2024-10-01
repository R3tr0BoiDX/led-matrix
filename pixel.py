from typing import Tuple, List

import colors


class Pixel:
    def __init__(self, color: Tuple[int, int, int]):
        self.color = color

    def __str__(self):
        return f"Pixel({self.color})"

    def __repr__(self):
        return self.__str__()


def clear_pixel_buffer(pixels: List[List[Pixel]]) -> None:
    for row in pixels:
        for pixel in row:
            pixel.color = colors.BACKGROUND_COLOR
