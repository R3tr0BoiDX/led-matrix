import os
import signal
import threading
import time
from datetime import datetime
from typing import List
import logging

import requests

import api
import buffer as buf
import colors
import graphics
import settings

# from effects.rain import RainEffect
# from effects.snow import SnowEffect
from pixel import Pixel
from weather import get_weather

INTERVAL_UPDATE_TIME = 1  # seconds
TARGET_FPS = 24  # frames per second

CLOCK_INITIAL_OFFSET = (3, 0)
WEATHER_OFFSET = (22, 0)
TIME_FORMAT = "%H:%M"

RUNNING = True

lock_time = threading.Lock()
lock_weather = threading.Lock()

# Set up logging
# todo: create better logger and use everywhere
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# todo: move to weather.py
class WeatherFetcher:
    def __init__(self):
        self.weather = None

    def get_weather_data(self):
        # Try fetching weather data
        try:
            self.weather = get_weather()
            logger.info("Weather data fetched")
        except requests.exceptions.RequestException as e:
            logger.error("Error fetching weather data: %s", e)

        # Set a timer to fetch data again
        threading.Timer(
            settings.get_weather_request_interval(), self.get_weather_data
        ).start()


def change_brightness(weather_data: WeatherFetcher):

    # Set a timer to update the brightness again
    # (based on weather request interval, as sunrise and sunset times are sourced from the weather data)
    threading.Timer(
        settings.get_weather_request_interval(), change_brightness, args=(weather_data,)
    ).start()

    # Check if weather data is available
    if not weather_data.weather:
        logger.error("Weather data not available")
        return

    # Get key times of the day
    now = int(time.time())
    sunrise = weather_data.weather.current.sunrise
    sunset = weather_data.weather.current.sunset

    # Log out if its day or night mode using a ternary operator
    logger.info("Now is day mode" if sunrise < now < sunset else "Now is night mode")

    # Get the brightness
    brightness = (
        settings.get_brightness_day()
        if sunrise < now < sunset
        else settings.get_brightness_night()
    )

    # Set the brightness
    buf.get_display().set_brightness(brightness)
    logger.info("Brightness set to %s", brightness)


def draw_time(buffer: List[List[Pixel]], show_colon: bool) -> None:
    # Create a new buffer based on the given buffer size
    work_buffer = buf.get_new_buffer(len(buffer[0]), len(buffer))

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
        graphics.draw_graphic(work_buffer, data, offset, colors.TIME_COLOR)
        offset = (offset[0] + len(data[0]) + 1, offset[1])

    with lock_time:
        # Copy the work buffer to the display buffer
        buf.copy_buffers(work_buffer, buffer)

    # Set a timer to update the time
    threading.Timer(
        INTERVAL_UPDATE_TIME, draw_time, args=(buffer, not show_colon)
    ).start()


def draw_weather(buffer: List[List[Pixel]], weather_data: WeatherFetcher) -> None:

    # Set a timer to update the time
    threading.Timer(
        INTERVAL_UPDATE_TIME, draw_weather, args=(buffer, weather_data)
    ).start()

    # Check if weather data is available
    if not weather_data.weather:
        logger.error("Weather data not available")
        return

    # Create a new buffer based on the given buffer size
    work_buffer = buf.get_new_buffer(len(buffer[0]), len(buffer))

    icon = weather_data.weather.current.weather[0].icon
    data = graphics.read_image(graphics.get_filepath(icon))
    graphics.draw_graphic(work_buffer, data, WEATHER_OFFSET)

    with lock_weather:
        # Copy the work buffer to the display buffer
        buf.copy_buffers(work_buffer, buffer)


def shutdown():
    # Clear the display and kill the process including all threads
    buf.shutdown()
    os.kill(os.getpid(), signal.SIGTERM)


def main():
    # Initialize data holder
    weather_data_provider = WeatherFetcher()

    # Start fetching weather data
    weather_data_provider.get_weather_data()

    # Get the display dimensions
    width = settings.get_display_width()
    height = settings.get_display_height()

    # Change brightness based on time of day
    if settings.get_change_brightness():
        change_brightness(weather_data_provider)

    # Draw time
    time_buffer = buf.get_new_buffer(width, height)
    draw_time(time_buffer, False)

    # Draw weather
    weather_buffer = buf.get_new_buffer(width, height)
    draw_weather(weather_buffer, weather_data_provider)

    # Initialize effects
    effect_buffer = buf.get_new_buffer(width, height)
    if settings.get_effects():
        # SnowEffect((width, height)).start(effect_buffer)
        # RainEffect((width, height)).start(effect_buffer)
        pass

    # Start the API server in a separate thread
    threading.Thread(target=api.run, args=(buf.get_display(),)).start()

    # Calculate the redraw interval
    redraw_interval = (1000 / settings.get_target_fps()) / 1000  # seconds

    # Main loop
    while RUNNING:
        # Write data to the buffer
        buf.write_to_buffer(effect_buffer)
        buf.write_to_buffer(weather_buffer)
        buf.write_to_buffer(time_buffer)

        # Display the buffer
        buf.display()

        # Clear the buffer
        buf.clear_buffer()

        # Prepare next iteration
        time.sleep(redraw_interval)

    # Unexpected shutdown
    shutdown()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down...")
        shutdown()
