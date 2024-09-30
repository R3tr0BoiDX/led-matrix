import threading
import time
from datetime import datetime
from typing import List, Tuple
import random

import graphics
from debug import DebugDisplay
from pixel import Pixel
from weather import WeatherData, get_weather

import random

GRAVITY = 1
SNOWFLAKE_COLOR = (196, 196, 196)

num_snowflakes = 10  # Adjust this number as desired
snowflakes = [
    Snowflake(
        random.randint(0, PIXEL_WIDTH - 1), random.randint(0, PIXEL_HEIGHT - 1)
    )
    for _ in range(num_snowflakes)
]

class Snowflake:
    def __init__(self, x, y):
        self.pos = (x, y)

    def fall(self, height):
        # Move the snowflake down
        self.pos = (self.pos[0] + random.randint(-1, 1), self.pos[1] + GRAVITY)

        if self.pos[0] < 0:
            self.pos = (0, self.pos[1])
        elif self.pos[0] >= 32:
            self.pos = (31, self.pos[1])

        # If it goes off screen, reset to the top
        if self.pos[1] >= height:
            self.pos = (random.randint(0, 32 - 1), 0)


def rain():
    print("It's raining!")

def snow():
        # TODO: I AM UGLY TOO, MAKE ME ALSO PRETTY
        # Update snowflakes
        for flake in snowflakes:
            flake.fall(PIXEL_HEIGHT)

        # Draw snowflakes
        for flake in snowflakes:
            pixels[flake.pos[1]][flake.pos[0]] = Pixel(
                SNOWFLAKE_COLOR
            )  # White color for snowflakes

        # Draw the solid white line at the bottom
        for x in range(PIXEL_WIDTH):
            pixels[PIXEL_HEIGHT - 1][x] = Pixel(
                SNOWFLAKE_COLOR
            )  # White color for the bottom line
        # TODO: NOT UGLY ANYMORE