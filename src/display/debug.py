import os
import platform
import signal
from typing import List

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

from src import colors, log
from src.display import base as display
from src.pixel import Pixel

PIXEL_SIZE = 40
WINDOW_CAPTION = "Matrix emulator"

# Initialize Pygame
pygame.init()

logger = log.get_logger(__name__)


class DebugDisplay(display.Display):

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.display_size = (width * PIXEL_SIZE, height * PIXEL_SIZE)
        self.screen = pygame.display.set_mode(self.display_size)
        pygame.display.set_caption(WINDOW_CAPTION)
        logger.info("Initialized debug display with size %s and name %s", self.display_size, WINDOW_CAPTION)

        # Set always on top based on platform
        window = pygame.display.get_wm_info()["window"]
        logger.debug("Window ID: %s", window)
        if platform.system() == "Linux":
            logger.info("Linux detected, setting window always on top")
            os.system(f"wmctrl -i -r {window} -b add,above")
            os.system(f"wmctrl -i -a {window}")
        elif platform.system() == "Windows":
            import ctypes

            logger.info("Windows detected, setting window always on top")
            ctypes.windll.user32.SetWindowPos(window, -1, 0, 0, 0, 0, 0x0001)

    def display(self):
        try:
            logger.debug("Displaying pixels")
            pygame.display.flip()
        except pygame.error as e:
            logger.debug("Error displaying pixels: %s", e)

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
            logger.debug("Updated pixels")
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
        except pygame.error as e:
            logger.debug("Error updating pixels: %s", e)

    def clear(self):
        try:
            logger.debug("Clearing screen")
            self.screen.fill(colors.BACKGROUND_COLOR)
        except pygame.error as e:
            logger.debug("Error clearing screen: %s", e)

    def shutdown(self):
        logger.debug("Cleaning screen and shutting down")
        self.clear()
        self.display()
        pygame.quit()
        # Kill to also stop threads
        os.kill(os.getpid(), signal.SIGTERM)

    def set_brightness(self, brightness: int):
        logger.info("Setting brightness to %s", brightness)
