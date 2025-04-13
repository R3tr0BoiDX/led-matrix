import os
import signal
import threading
import time
from datetime import datetime
from typing import List

from src import api
from src import buffer as buf
from src import colors, graphics, log, settings, network_status
from src.pixel import Pixel
from src.weather import WeatherProvider

# from src.effects.rain import RainEffect
# from src.effects.snow import SnowEffect

RUNNING = True

lock_time = threading.Lock()
lock_weather = threading.Lock()

# Set up logging
log.setup_logging()
logger = log.get_logger(__name__)


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
    logger.debug("Sunrise: %s, Sunset: %s, Now: %s", sunrise, sunset, now)

    # Get the brightness
    brightness = (
        settings.Display().get_brightness_day()
        if sunrise < now < sunset
        else settings.Display().get_brightness_night()
    )

    # Set the brightness
    logger.info(
        "Setting brightness to %s",
        "day mode" if sunrise < now < sunset else "night mode",
    )
    buf.get_display().set_brightness(brightness)


def draw_network_status(buffer: List[List[Pixel]]) -> None:
    # Create a new buffer based on the given buffer size
    work_buffer = buf.get_new_buffer(len(buffer[0]), len(buffer))
    logger.debug("Creating new buffer with size %s x %s", len(buffer[0]), len)

    # Update the network status
    offset = (
        settings.Network().get_indicator_x(),
        settings.Network().get_indicator_y(),
    )
    color = settings.Network().get_indicator_disconnect_color()
    if network_status.ping_host():
        color = settings.Network().get_indicator_connect_color()
        logger.debug("Network status: connected")
    else:
        logger.info("Network status: disconnected")

    # Draw the network status indicator
    graphics.draw_pixel(
        work_buffer,
        offset,
        color,
    )

    # Set timer to update the network status
    threading.Timer(
        settings.Network().get_check_interval(),
        draw_network_status,
        args=(buffer,),
    ).start()

    # Copy the work buffer to the display buffer
    # Hence its just a single pixel, we can just copy it directly. No lock needed.
    buf.copy_buffers(work_buffer, buffer)
    logger.debug("Copying work buffer to display buffer")


def draw_char(
    buffer: List[List[Pixel]], char: str, offset: tuple, offset_delta: int
) -> tuple:
    data = graphics.read_image(graphics.get_filepath(char))
    graphics.draw_graphic(buffer, data, offset, colors.TIME_COLOR)
    offset = (offset[0] + len(data[0]) + offset_delta, offset[1])
    logger.debug(
        "Drawing character %s, adding %s to offset", char, len(data[0]) + offset_delta
    )
    return offset


def draw_time(buffer: List[List[Pixel]], show_colon: bool) -> None:
    # Create a new buffer based on the given buffer size
    work_buffer = buf.get_new_buffer(len(buffer[0]), len(buffer))
    logger.debug("Creating new buffer with size %s x %s", len(buffer[0]), len)

    # Update the on-screen time
    now = datetime.now().strftime(settings.Clock().get_time_format())
    offset = (settings.Clock().get_offset_x(), settings.Clock().get_offset_y())
    offset_char = settings.Clock().get_offset_delta()

    logger.debug("Drawing time %s", now)
    for char in str(now):

        # Handle the colon character specially
        if char == ":":

            # Check if the colon should be shown
            show_seconds = settings.Clock().show_seconds()
            if not show_seconds:
                continue

            # Draw the colon character
            if show_colon:
                char = "colon"
                logger.debug("Drawing colon")
            else:
                offset = (offset[0] + offset_char + 1, offset[1])
                logger.debug("Skipping colon, adding %s to offset", offset_char + 1)
                continue

        # Draw the character
        offset = draw_char(work_buffer, char, offset, offset_char)

    with lock_time:
        # Copy the work buffer to the display buffer
        buf.copy_buffers(work_buffer, buffer)
        logger.debug("Copying work buffer to display buffer")

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
    logger.debug("Creating new buffer with size %s x %s", len(buffer[0]), len)

    # Draw the first weather element
    offset = (settings.Weather().get_offset_x(), settings.Weather().get_offset_y())
    if settings.Weather().swap_icon_temp():
        offset = draw_weather_temp(work_buffer, weather_data, offset)
    else:
        offset = draw_weather_icon(work_buffer, weather_data, offset)

    # Draw the second weather element
    offset = (offset[0] + settings.Weather().get_offset_between(), offset[1])
    if settings.Weather().swap_icon_temp():
        offset = draw_weather_icon(work_buffer, weather_data, offset)
    else:
        offset = draw_weather_temp(work_buffer, weather_data, offset)

    with lock_weather:
        # Copy the work buffer to the display buffer
        buf.copy_buffers(work_buffer, buffer)
        logger.debug("Copying work buffer to display buffer")


def draw_weather_icon(
    buffer: List[List[Pixel]], weather_data: WeatherProvider, offset: tuple
) -> tuple:
    if not settings.Weather().show_icon():
        return offset

    icon = weather_data.weather.current.weather[0].icon
    data = graphics.read_image(graphics.get_filepath(icon))
    graphics.draw_graphic(buffer, data, offset)
    offset = (offset[0] + len(data[0]), offset[1])
    logger.debug("Drawing weather icon %s", icon)
    return offset


def draw_weather_temp(
    buffer: List[List[Pixel]], weather_data: WeatherProvider, offset: tuple
) -> tuple:
    if not settings.Weather().show_temp():
        return offset

    # Format the temperature
    temp = weather_data.weather.current.temp
    temp = str(round(weather_data.weather.current.temp)).rjust(2, "x") + "°"
    logger.debug("Drawing temperature %s", temp)

    # Draw the temperature
    offset_char = settings.Weather().get_offset_delta()
    for i, char in enumerate(temp):

        # When the character is a x, skip it, just add offset
        if char == "x":
            offset = (offset[0] + offset_char + 2, offset[1])
            logger.debug("Skipping x, adding %s to offset", offset_char)
            continue

        # Handle the degree character specially
        if char == "°":
            char = "degree"
            logger.debug("Drawing degree symbol")

        # Check if the character is not the last one
        if i != len(temp) - 1:
            # Draw the character
            offset = draw_char(buffer, char, offset, offset_char)
        else:
            # Draw the character and, but remove delta offset
            offset = draw_char(buffer, char, offset, offset_char)
            offset = (offset[0] - offset_char, offset[1])  # a lil hacky, but ehh

    return offset


def shutdown():
    # Clear the display and kill the process including all threads
    logger.info("Shutting down...")
    buf.shutdown()
    os.kill(os.getpid(), signal.SIGTERM)


def main():
    # Initialize weather provider
    logger.debug("Initializing weather provider")
    weather_provider = WeatherProvider()

    # Start fetching weather data
    logger.info("Start fetching weather data")
    weather_provider.get_weather_data()

    # Get the display dimensions
    width = settings.Display().get_width()
    height = settings.Display().get_height()
    logger.debug("Display dimensions: %s x %s", width, height)

    # Change brightness based on time of day
    if settings.Display().get_change_brightness():
        logger.info("Start observing daytime for brightness changes")
        change_brightness(weather_provider)

    # Draw time
    time_buffer = buf.get_new_buffer(width, height)
    if settings.Clock().show_clock():
        logger.info("Start drawing time")
        draw_time(time_buffer, False)

    # Draw weather
    weather_buffer = buf.get_new_buffer(width, height)
    if settings.Weather().show_icon() or settings.Weather().show_temp():
        logger.info("Start drawing weather")
        draw_weather(weather_buffer, weather_provider)

    # Draw network status
    network_buffer = buf.get_new_buffer(width, height)
    if settings.Network().show_indicator():
        logger.info("Start drawing network status")
        draw_network_status(network_buffer)

    # Initialize effects
    effect_buffer = buf.get_new_buffer(width, height)
    if settings.Weather().get_effects():
        logger.info("Start drawing weather effects")
        # SnowEffect((width, height)).start(effect_buffer)
        # RainEffect((width, height)).start(effect_buffer)

    # Start the API server in a separate thread
    logger.info("Starting API server")
    threading.Thread(target=api.run, args=(buf.get_display(),)).start()

    # Calculate the redraw interval
    redraw_interval = (1000 / settings.Display().get_target_fps()) / 1000  # seconds
    logger.debug("Redraw interval: %s", redraw_interval)

    # Main loop
    while RUNNING:
        # Write data to the buffer
        buf.write_to_buffer(effect_buffer)
        buf.write_to_buffer(network_buffer)
        buf.write_to_buffer(weather_buffer)
        buf.write_to_buffer(time_buffer)

        # Display the buffer
        buf.display()

        # Clear the buffer
        buf.clear_buffer()

        # Prepare next iteration
        time.sleep(redraw_interval)

    # Unexpected shutdown
    logger.critical("Main loop exited unexpectedly due to stray cosmic rays!")
    shutdown()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        shutdown()
