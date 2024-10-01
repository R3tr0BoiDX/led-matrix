import sys
import threading
import time
from datetime import datetime
from typing import List, Tuple

import requests

import colors
import graphics
from debug import DebugDisplay
from pixel import Pixel, clear_pixel_buffer
from weather import WeatherData, get_weather
from effects.snow import SnowEffect

DEBUG_MODE = True
PIXEL_HEIGHT = 8
PIXEL_WIDTH = 32

INTERVAL_REQUEST_DATA = 120  # seconds
INTERVAL_UPDATE_TIME = 1  # seconds
INTERVAL_REDRAW = 0.1  # seconds  # 0.033 for 30fps

CLOCK_INITIAL_OFFSET = (7, 0)
WEATHER_OFFSET = (22, 0)

TIME_FORMAT = "%H:%M"

RUNNING = True


def draw_graphic(
    pixels: List[List[Pixel]],
    data: List[List[Pixel]],
    offset: Tuple[int, int],
) -> None:

    x_offset, y_offset = offset

    for y, row in enumerate(data):
        for x, pixel in enumerate(row):
            if y + y_offset < len(pixels) and x + x_offset < len(pixels[0]):
                if pixel.color != colors.TRANSPARENT_COLOR:
                    pixels[y + y_offset][x + x_offset] = pixel


def draw_time(pixels: List[List[Pixel]], show_colon: bool) -> None:
    # Clear the pixel buffer content from previous iteration
    clear_pixel_buffer(pixels)

    # Update the on-screen time
    now = datetime.now().strftime(TIME_FORMAT)
    offset = CLOCK_INITIAL_OFFSET
    for char in str(now):
        if char == ":":
            if show_colon:
                char = "colon"
            else:
                offset = (offset[0] + 2, offset[1])
                continue
        data = graphics.read_image(graphics.get_filepath(char))
        draw_graphic(pixels, data, offset)
        offset = (offset[0] + len(data[0]) + 1, offset[1])

    # Set a timer to update the time
    threading.Timer(
        INTERVAL_UPDATE_TIME, draw_time, args=(pixels, not show_colon)
    ).start()


def draw_weather(pixels: List[List[Pixel]], weather_data: WeatherData) -> None:
    icon = weather_data.current.weather[0].icon
    data = graphics.read_image(graphics.get_filepath(icon))
    draw_graphic(pixels, data, WEATHER_OFFSET)


class WeatherFetcher:
    def __init__(self):
        self.weather = None

    def get_weather_data(self):
        # Try fetching weather data
        try:
            self.weather = get_weather()
        except requests.exceptions.RequestException as e:
            print("Error fetching weather data:", e)

        # Set a timer to fetch data again
        threading.Timer(INTERVAL_REQUEST_DATA, self.get_weather_data).start()


def main():
    # Initialize data holder
    data_holder = WeatherFetcher()

    # Start fetching weather data
    data_holder.get_weather_data()

    # Initialize buffer and start drawing
    time_buffer = [
        [Pixel(colors.BACKGROUND_COLOR) for x in range(PIXEL_WIDTH)]
        for y in range(PIXEL_HEIGHT)
    ]
    draw_time(time_buffer, False)

    # Initialize pixel buffer
    effect_buffer = [
        [Pixel(colors.BACKGROUND_COLOR) for x in range(PIXEL_WIDTH)]
        for y in range(PIXEL_HEIGHT)
    ]
    SnowEffect((PIXEL_WIDTH, PIXEL_HEIGHT)).start(effect_buffer)

    # Start updating weather
    # if data_holder.weather:
    #     # todo: needs timer update like time
    #     draw_weather(pixels, data_holder.weather)

    if DEBUG_MODE:
        display = DebugDisplay()
    else:
        # todo: implement hardware.py
        # from hardware import Display
        # display = Display()
        pass

    # Main loop
    while RUNNING:
        # Clear the pixel and
        display.clear()

        # Update display
        # todo: merge the buffers and update once
        display.update(effect_buffer)
        display.update(time_buffer)

        # Display the content
        display.display()

        # Prepare next iteration
        time.sleep(INTERVAL_REDRAW)

    display.exit()
    sys.exit()


if __name__ == "__main__":
    main()
