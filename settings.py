import yaml

SETTINGS_FILE = "settings.yaml"

SETTINGS = {}
with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
    SETTINGS = yaml.safe_load(file)


def get_latitude():
    return SETTINGS.get("latitude")


def get_longitude():
    return SETTINGS.get("longitude")


def get_exclude():
    return SETTINGS.get("exclude")


def get_units():
    return SETTINGS.get("units")


def get_language():
    return SETTINGS.get("language")


def get_weather_request_interval():
    return SETTINGS.get("weather_request_interval")


def get_api_key():
    return SETTINGS.get("api_key")


def get_display_height():
    return SETTINGS.get("display_height")


def get_display_width():
    return SETTINGS.get("display_width")


def get_target_fps():
    return SETTINGS.get("target_fps")
