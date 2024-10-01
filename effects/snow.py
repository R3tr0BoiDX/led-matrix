import random
import threading
from typing import List, Tuple

from effects import base
from pixel import Pixel, clear_pixel_buffer
import colors

GRAVITY = 1
SNOWFLAKE_COLOR = colors.P8_WHITE
SNOWFLAKES_COUNT = 20

INTERVAL_UPDATE_TIME = 0.7


class Snowflake:
    def __init__(self, x, y):
        self.pos = (x, y)

    def fall(self, height):
        # Move the snowflake down
        jitter = random.choices([-1, 0, 1], weights=[10, 80, 10], k=1)[0]
        self.pos = (
            self.pos[0] + jitter,
            self.pos[1] + GRAVITY,
        )

        if self.pos[0] < 0:
            self.pos = (0, self.pos[1])
        elif self.pos[0] >= 32:
            self.pos = (31, self.pos[1])

        # If it goes off screen, reset to the top
        if self.pos[1] >= height:
            self.pos = (random.randint(0, 32 - 1), 0)


class SnowEffect(base.Effect):

    def __init__(self, dimensions: Tuple[int, int]):
        self.dimensions = dimensions

        width, height = dimensions
        self.snowflakes = [
            Snowflake(random.randint(0, width - 1), random.randint(0, height - 1))
            for _ in range(SNOWFLAKES_COUNT)
        ]

    def start(self, buffer: List[List[Pixel]]):
        # Clear the pixel buffer content from previous iteration
        clear_pixel_buffer(buffer)

        # Draw the solid white line at the bottom
        for x in range(self.dimensions[0]):
            buffer[self.dimensions[1] - 1][x] = Pixel(SNOWFLAKE_COLOR)

        # Update snowflakes
        for flake in self.snowflakes:
            flake.fall(self.dimensions[1])

        # Draw snowflakes
        for flake in self.snowflakes:
            buffer[flake.pos[1]][flake.pos[0]] = Pixel(SNOWFLAKE_COLOR)

        # Set a timer to update the time
        threading.Timer(INTERVAL_UPDATE_TIME, self.start, args=(buffer,)).start()
