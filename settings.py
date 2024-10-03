import yaml

SETTINGS_FILE = "settings.yaml"

SETTINGS = {}
with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
    SETTINGS = yaml.safe_load(file)


def get_debug() -> bool:
    return SETTINGS.get("debug")


def get_latitude() -> float:
    return SETTINGS.get("latitude")


def get_longitude() -> float:
    return SETTINGS.get("longitude")


def get_exclude() -> str:
    return SETTINGS.get("exclude")


def get_units() -> str:
    return SETTINGS.get("units")


def get_language() -> str:
    return SETTINGS.get("language")


def get_weather_request_interval() -> int:
    return SETTINGS.get("weather_request_interval")


def get_api_key() -> str:
    return SETTINGS.get("api_key")


def get_display_height() -> int:
    return SETTINGS.get("display_height")


def get_display_width() -> int:
    return SETTINGS.get("display_width")


def get_target_fps() -> int:
    return SETTINGS.get("target_fps")


def get_effect() -> bool:
    return SETTINGS.get("effects")
