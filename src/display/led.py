import time
from typing import List, Tuple

from rpi_ws281x import Color, PixelStrip

from src import colors, settings, log
from src.display import base as display
from src.pixel import Pixel

logger = log.get_logger(__name__)


def _led_matrix_translation(pos: Tuple[int, int], size: Tuple[int, int]) -> int:
    x, y = pos
    _, height = size
    index = 0
    if _number_is_even(x):
        index = x * height + y
    else:
        index = x * height + height - 1 - y

    logger.debug("LED matrix translation: %s -> %s", pos, index)
    return index


def _number_is_even(number: int) -> bool:
    return number % 2 == 0


def _color_translation(color: Tuple[int, int, int]) -> Color:
    r, g, b = color
    return Color(r, g, b)


class LedDisplay(display.Display):
    def __init__(self, size: Tuple[int, int]):
        self.size = size
        self.ledCount = size[0] * size[1]

        # Create pixel object
        # todo: gamma
        self.leds = PixelStrip(
            self.ledCount,
            settings.Display().get_pin(),
            settings.Display().get_target_frequency(),
            settings.Display().get_dma(),
            settings.Display().get_inverted(),
            settings.Display().get_brightness_day(),
            settings.Display().get_channel(),
            settings.Display().get_strip_type(),
            # look at the rpi_ws281x documentation for more options
            # https://github.com/jgarff/rpi_ws281x/blob/1f47b59ed603223d1376d36c788c89af67ae2fdc/ws2811.h#L47
        )
        logger.info(
            (
                "LED display initialized with settings: "
                "Pin: %s, Frequency: %s, DMA: %s, Inverted: %s, Brightness: %s, Channel: %s, Strip type: %s"
            ),
            settings.Display().get_pin(),
            settings.Display().get_target_frequency(),
            settings.Display().get_dma(),
            settings.Display().get_inverted(),
            settings.Display().get_brightness_day(),
            settings.Display().get_channel(),
            settings.Display().get_strip_type(),
        )

        # Initialize the library (must be called once before other functions)
        self.leds.begin()

        # Clear the display on startup
        self.clear()

    def display(self):
        logger.debug("Displaying pixels")
        self.leds.show()

    def update(self, pixel_array: List[List[Pixel]]):
        logger.debug("Updating pixels")
        for y, row in enumerate(pixel_array):
            for x, pixel in enumerate(row):
                if pixel.color != colors.TRANSPARENT_COLOR:
                    self.set_pixel((x, y), _color_translation(pixel.color))

    def clear(self):
        logger.debug("Clearing pixels")
        for i in range(self.leds.numPixels()):
            r, g, b = colors.BACKGROUND_COLOR
            self.leds.setPixelColor(i, Color(r, g, b))

    def shutdown(self):
        logger.debug("Cleaning LEDs before shutdown")
        self.clear()
        self.display()

    def set_pixel(self, pos: Tuple[int, int], color: Color):
        logger.debug("Setting pixel at %s to color %s", pos, color)
        self.leds.setPixelColor(_led_matrix_translation(pos, self.size), color)

    def set_brightness(self, brightness: int):
        logger.info("Setting brightness to %s", brightness)
        self.leds.setBrightness(brightness)

    # Demo function to test the LED display
    def demo(self):
        logger.info("Running LED display demo")
        for i in range(self.leds.numPixels()):
            self.leds.setPixelColor(i, Color(255, 255, 255))
            self.leds.show()
            time.sleep(0.1)
            self.leds.setPixelColor(i, Color(0, 0, 0))
            self.leds.show()


if __name__ == "__main__":
    logger.info("Running LED display test")
    try:
        leds = LedDisplay((settings.Display().get_width(), settings.Display().get_height()))
        leds.demo()
        leds.shutdown()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt detected, shutting down...")
        leds.shutdown()
