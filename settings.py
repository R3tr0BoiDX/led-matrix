import yaml

SETTINGS_FILE = "settings.yaml"

_settings = {}
with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
    _settings = yaml.safe_load(file)


def get_debug() -> bool:
    return _settings.get("debug")


def get_latitude() -> float:
    return _settings.get("latitude")


def get_longitude() -> float:
    return _settings.get("longitude")


def get_exclude() -> str:
    return _settings.get("exclude")


def get_units() -> str:
    return _settings.get("units")


def get_language() -> str:
    return _settings.get("language")


def get_weather_request_interval() -> int:
    return _settings.get("weather_request_interval")


def get_api_key() -> str:
    return _settings.get("api_key")


def get_display_height() -> int:
    return _settings.get("display_height")


def get_display_width() -> int:
    return _settings.get("display_width")


def get_target_fps() -> int:
    return _settings.get("target_fps")


def get_effect() -> bool:
    return _settings.get("effects")


def get_pin() -> int:
    return _settings.get("pin")


def get_target_frequency() -> int:
    return _settings.get("target_frequency")


def get_dma() -> int:
    return _settings.get("dma")


def get_strip_type() -> int:
    return _settings.get("strip_type")


def get_inverted() -> int:
    return _settings.get("inverted")


def get_brightness_day() -> int:
    return _settings.get("brightness_day")


def get_brightness_night() -> int:
    return _settings.get("brightness_night")


def get_change_brightness() -> bool:
    return _settings.get("change_brightness")


def get_channel() -> int:
    return _settings.get("channel")
