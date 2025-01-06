import random
import threading
from typing import List, Tuple

from src import buffer as buf
from src import colors, graphics
from src.effects import base
from src.pixel import Pixel

RAIN_COLOR = colors.P8_DARK_BLUE

GRAVITY = 1
RAINDROP_COUNT = 16

UMBRELLA_GRAPHIC = "umbrella"
UMBRELLA_OFFSET = (22, 0)
INTERVAL_UPDATE_TIME = 0.1  # seconds

# Maximum number of tries to place a raindrop without overlap
MAX_TRIES = 16


class Raindrop:
    def __init__(self, x, y):
        self.pos = (x, y)

    def fall(self, dimensions: Tuple[int, int], occupied_x: set):
        width, height = dimensions

        # Move the raindrop down
        self.pos = (
            self.pos[0],
            self.pos[1] + GRAVITY,
        )

        # If it goes off screen, reset to the top with no neighboring raindrops
        if self.pos[1] >= height + 1:
            self.respawn_at_top(width, occupied_x)

    def respawn_at_top(self, width: int, occupied_x: set):
        while True:
            x = random.randint(0, width - 1)
            # Ensure no neighboring raindrops
            if (
                x not in occupied_x
                and (x - 1) not in occupied_x
                and (x + 1) not in occupied_x
            ):
                self.pos = (x, 0)
                occupied_x.add(x)  # Mark this x-coordinate as occupied
                break


class RainEffect(base.Effect):
    def __init__(self, dimensions: Tuple[int, int]):
        self.dimensions = dimensions
        self.lock = threading.Lock()

        self.raindrops = self.generate_raindrops(
            self.dimensions[0], self.dimensions[1], RAINDROP_COUNT
        )

    def generate_raindrops(self, width: int, height: int, count: int) -> List[Raindrop]:
        occupied_x = set()
        raindrops = []

        # Generate raindrops
        while len(raindrops) < count:

            # Try to place a raindrop
            for tries in range(MAX_TRIES + 1):

                # Randomly place a raindrop
                x = random.randint(0, width - 1)

                # Ensure no neighboring raindrops
                if (
                    x not in occupied_x
                    and (x - 1) not in occupied_x
                    and (x + 1) not in occupied_x
                ):
                    # Add the raindrop and mark the x-coordinate as occupied
                    occupied_x.add(x)
                    y = random.randint(0, height - 1)
                    raindrops.append(Raindrop(x, y))
                    break

            if tries == MAX_TRIES:
                break

        return raindrops

    def start(self, buffer: List[List[Pixel]]):

        # Create the work buffer
        work_buffer = buf.get_new_buffer(self.dimensions[0], self.dimensions[1])

        # Track x-coordinates where raindrops are at the top
        occupied_x = set()

        # Update raindrops
        for drop in self.raindrops:
            drop.fall(self.dimensions, occupied_x)

        # Draw raindrops
        for drop in self.raindrops:
            if drop.pos[1] < self.dimensions[1]:
                work_buffer[drop.pos[1]][drop.pos[0]] = Pixel(RAIN_COLOR)
            if drop.pos[1] > 0:
                work_buffer[drop.pos[1] - 1][drop.pos[0]] = Pixel(RAIN_COLOR)

        # Draw the umbrella
        graphics.draw_graphic(
            work_buffer,
            graphics.read_image(graphics.get_filepath(UMBRELLA_GRAPHIC)),
            UMBRELLA_OFFSET,
        )

        with self.lock:
            # Copy the work buffer to the display buffer
            buf.copy_buffers(work_buffer, buffer)

        # Set a timer to update the time
        threading.Timer(INTERVAL_UPDATE_TIME, self.start, args=(buffer,)).start()
