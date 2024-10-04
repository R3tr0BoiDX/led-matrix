from typing import Tuple
import time

import _rpi_ws281x as ws281x
from rpi_ws281x import Color, PixelStrip

# TODO: source from settings
LED_HEIGHT = 8
LED_WIDTH = 32

TARGET_FREQ = ws281x.WS2811_TARGET_FREQ
GPIO_PIN = 18  # todo: add to settings
DMA = 10
LED_COUNT = LED_WIDTH * LED_HEIGHT
STRIP_TYPE = ws281x.WS2812_STRIP
INVERTED = False
BRIGHTNESS = 255
CHANNEL = 0


def clear(leds: PixelStrip):
    for i in range(leds.numPixels()):
        leds.setPixelColor(i, Color(0, 0, 0))
    leds.show()


def flush(leds: PixelStrip):
    for i in range(leds.numPixels()):
        leds.setPixelColor(i, Color(0, 0, 0))


def set_pixel(pos: Tuple[int, int], color: Color, leds: PixelStrip):
    leds.setPixelColor(led_matrix_translation(pos), color)


def set_brightness(brightness: int, leds: PixelStrip):
    leds.setBrightness(brightness)


def led_matrix_translation(pos: Tuple[int, int]) -> int:
    x, y = pos
    if _number_is_even(x):
        return x * LED_HEIGHT + y
    else:
        return x * LED_HEIGHT + LED_HEIGHT - 1 - y


def _number_is_even(number: int) -> bool:
    return number % 2 == 0


# TODO: impl the display interface
class LedDisplay:
    def __init__(self):
        # Create pixel object
        self.leds = PixelStrip(
            LED_COUNT,
            GPIO_PIN,
            TARGET_FREQ,
            DMA,
            INVERTED,
            BRIGHTNESS,
            CHANNEL,
            strip_type=STRIP_TYPE,
        )

        # Initialize the library (must be called once before other functions)
        self.leds.begin()

        # Clear the display on startup
        clear(self.leds)

    def shutdown(self):
        clear(self.leds)

    def demo(self):
        for i in range(self.leds.numPixels()):
            self.leds.setPixelColor(i, Color(255, 255, 255))
            self.leds.show()
            time.sleep(0.1)
            self.leds.setPixelColor(i, Color(0, 0, 0))
            self.leds.show()


if __name__ == "__main__":
    try:
        matrix = LedDisplay()
        matrix.demo()
        matrix.shutdown()
    except KeyboardInterrupt:
        matrix.shutdown()
        print("Exiting...")
