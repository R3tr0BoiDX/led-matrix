import sys
import threading
import time
from datetime import datetime
from typing import List

import requests

import colors
import graphics
import settings
from effects.snow import SnowEffect
from effects.rain import RainEffect
from pixel import Pixel, clear_pixel_buffer
from weather import WeatherData, get_weather
import buffer

INTERVAL_UPDATE_TIME = 1  # seconds
TARGET_FPS = 24  # frames per second

CLOCK_INITIAL_OFFSET = (3, 0)
WEATHER_OFFSET = (22, 0)
TIME_FORMAT = "%H:%M"

RUNNING = True


def draw_time(pixels: List[List[Pixel]], show_colon: bool) -> None:
    # Clear the pixel buffer content from previous iteration
    clear_pixel_buffer(pixels)

    # Update the on-screen time
    now = datetime.now().strftime(TIME_FORMAT)
    offset = CLOCK_INITIAL_OFFSET
    for char in str(now):

        # Handle the colon character specially
        if char == ":":
            if show_colon:
                char = "colon"
            else:
                offset = (offset[0] + 2, offset[1])
                continue

        # Draw the character
        data = graphics.read_image(graphics.get_filepath(char))
        graphics.draw_graphic(pixels, data, offset, colors.TIME_COLOR)
        offset = (offset[0] + len(data[0]) + 1, offset[1])

    # Set a timer to update the time
    threading.Timer(
        INTERVAL_UPDATE_TIME, draw_time, args=(pixels, not show_colon)
    ).start()


def draw_weather(pixels: List[List[Pixel]], weather_data: WeatherData) -> None:
    icon = weather_data.current.weather[0].icon
    data = graphics.read_image(graphics.get_filepath(icon))
    graphics.draw_graphic(pixels, data, WEATHER_OFFSET)


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
        threading.Timer(
            settings.get_weather_request_interval(), self.get_weather_data
        ).start()


def main():
    # Initialize data holder
    data_holder = WeatherFetcher()

    # Start fetching weather data
    data_holder.get_weather_data()

    # Get the display dimensions
    width = settings.get_display_width()
    height = settings.get_display_height()

    # Initialize buffer and start drawing
    time_buffer = [
        [Pixel(colors.BACKGROUND_COLOR) for _ in range(width)] for _ in range(height)
    ]
    draw_time(time_buffer, False)

    # Initialize effects
    effect_buffer = buffer.get_new_buffer(width, height)
    # SnowEffect((width, height)).start(effect_buffer)
    RainEffect((width, height)).start(effect_buffer)

    # Start updating weather
    # if data_holder.weather:
    #     # todo: needs timer update like time
    #     draw_weather(pixels, data_holder.weather)

    redraw_interval = (1000 / settings.get_target_fps()) / 1000  # seconds

    # Main loop
    while RUNNING:
        # Write data to the buffer
        buffer.BUFFER_MANAGER.write_to_buffer(effect_buffer)
        buffer.BUFFER_MANAGER.write_to_buffer(time_buffer)

        # Display the buffer
        buffer.display_buffer()

        # Prepare next iteration
        time.sleep(redraw_interval)

    buffer.shutdown()


if __name__ == "__main__":
    main()
