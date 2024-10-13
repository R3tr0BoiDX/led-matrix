import os
import signal
from typing import List

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

import colors
import display.base as display
from pixel import Pixel

PIXEL_SIZE = 40

# Initialize Pygame
pygame.init()


class DebugDisplay(display.Display):

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.display_size = (width * PIXEL_SIZE, height * PIXEL_SIZE)
        self.screen = pygame.display.set_mode(self.display_size)
        pygame.display.set_caption("Matrix emulator")

    def display(self):
        try:
            pygame.display.flip()
        except pygame.error:
            pass

    def update(self, pixel_array: List[List[Pixel]]):
        try:
            # Check for quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.shutdown()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.shutdown()

            # Draw the pixels
            for y, row in enumerate(pixel_array):
                for x, pixel in enumerate(row):
                    if pixel.color != colors.TRANSPARENT_COLOR:
                        pygame.draw.rect(
                            self.screen,
                            pixel.color,
                            pygame.Rect(
                                x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE
                            ),
                        )
        except pygame.error:
            pass

    def clear(self):
        try:
            self.screen.fill(colors.BACKGROUND_COLOR)
        except pygame.error:
            pass

    def shutdown(self):
        self.clear()
        self.display()
        pygame.quit()
        # Kill to also stop threads
        os.kill(os.getpid(), signal.SIGTERM)

    def set_brightness(self, brightness: int):
        print(f"Setting brightness to {brightness}")
