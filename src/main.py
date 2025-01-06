import logging
import os
import signal
import threading
import time
from datetime import datetime
from typing import List

from src import buffer as buf
from src import api, colors, graphics, settings
from src.pixel import Pixel
from src.weather import WeatherProvider

# from src.effects.rain import RainEffect
# from src.effects.snow import SnowEffect

RUNNING = True

lock_time = threading.Lock()
lock_weather = threading.Lock()

# Set up logging
# todo: create better logger and use everywhere
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def change_brightness(weather_data: WeatherProvider):

    # Set a timer to update the brightness again
    # (based on weather request interval, as sunrise and sunset times are sourced from the weather data)
    threading.Timer(
        settings.Weather().get_request_interval(),
        change_brightness,
        args=(weather_data,),
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
        settings.Display().get_brightness_day()
        if sunrise < now < sunset
        else settings.Display().get_brightness_night()
    )

    # Set the brightness
    buf.get_display().set_brightness(brightness)
    logger.info("Brightness set to %s", brightness)


def draw_time(buffer: List[List[Pixel]], show_colon: bool) -> None:
    # Create a new buffer based on the given buffer size
    work_buffer = buf.get_new_buffer(len(buffer[0]), len(buffer))

    # Update the on-screen time
    now = datetime.now().strftime(settings.Clock().get_time_format())
    offset = (settings.Clock().get_offset_x(), settings.Clock().get_offset_y())
    for char in str(now):
        offset_char = settings.Clock().get_offset_delta()

        # Handle the colon character specially
        if char == ":":

            # Check if the colon should be shown
            show_seconds = settings.Clock().show_seconds()
            if not show_seconds:
                continue

            # Draw the colon character
            if show_colon:
                char = "colon"
            else:
                offset = (offset[0] + offset_char + 1, offset[1])
                continue

        # Draw the character
        data = graphics.read_image(graphics.get_filepath(char))
        graphics.draw_graphic(work_buffer, data, offset, colors.TIME_COLOR)
        offset_char = settings.Clock().get_offset_delta()
        offset = (offset[0] + len(data[0]) + offset_char, offset[1])

    with lock_time:
        # Copy the work buffer to the display buffer
        buf.copy_buffers(work_buffer, buffer)

    # Set a timer to update the time
    threading.Timer(
        settings.Display().get_content_refresh_rate(),
        draw_time,
        args=(buffer, not show_colon),
    ).start()


def draw_weather(buffer: List[List[Pixel]], weather_data: WeatherProvider) -> None:

    # Set a timer to update the time
    threading.Timer(
        settings.Display().get_content_refresh_rate(),
        draw_weather,
        args=(buffer, weather_data),
    ).start()

    # Check if weather data is available
    if not weather_data.weather:
        logger.error("Weather data not available")
        return

    # Create a new buffer based on the given buffer size
    work_buffer = buf.get_new_buffer(len(buffer[0]), len(buffer))

    # Draw the weather icon
    if settings.Weather().show_icon():
        icon = weather_data.weather.current.weather[0].icon
        data = graphics.read_image(graphics.get_filepath(icon))
        offset = (settings.Weather().get_offset_x(), settings.Weather().get_offset_y())
        graphics.draw_graphic(work_buffer, data, offset)

    # Draw the temperature
    if settings.Weather().show_temp():
        temp = weather_data.weather.current.temp
        # todo: generic string drawing function
        print(temp)

    with lock_weather:
        # Copy the work buffer to the display buffer
        buf.copy_buffers(work_buffer, buffer)


def shutdown():
    # Clear the display and kill the process including all threads
    buf.shutdown()
    os.kill(os.getpid(), signal.SIGTERM)


def main():
    # Initialize data holder
    weather_provider = WeatherProvider()

    # Start fetching weather data
    weather_provider.get_weather_data()

    # Get the display dimensions
    width = settings.Display().get_width()
    height = settings.Display().get_height()

    # Change brightness based on time of day
    if settings.Display().get_change_brightness():
        change_brightness(weather_provider)

    # Draw time
    time_buffer = buf.get_new_buffer(width, height)
    if settings.Clock().show_clock():
        draw_time(time_buffer, False)

    # Draw weather
    weather_buffer = buf.get_new_buffer(width, height)
    draw_weather(weather_buffer, weather_provider)

    # Initialize effects
    effect_buffer = buf.get_new_buffer(width, height)
    if settings.Weather().get_effects():
        # SnowEffect((width, height)).start(effect_buffer)
        # RainEffect((width, height)).start(effect_buffer)
        pass

    # Start the API server in a separate thread
    threading.Thread(target=api.run, args=(buf.get_display(),)).start()

    # Calculate the redraw interval
    redraw_interval = (1000 / settings.Display().get_target_fps()) / 1000  # seconds

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
