import yaml

SETTINGS_FILE = "settings.yaml"

_settings = {}
try:
    with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
        _settings = yaml.safe_load(file)
except FileNotFoundError as e:
    raise FileNotFoundError(f"Error: {SETTINGS_FILE} not found.") from e
except yaml.YAMLError as e:
    raise ValueError(f"Error parsing {SETTINGS_FILE}") from e


# Helper function to navigate nested dictionaries using a path
def get_value(path: str):
    keys = path.split("/")
    value = _settings
    try:
        for key in keys:
            value = value[key]
        return value
    except KeyError as e:
        raise KeyError(f"Missing required setting for YAML path: '{path}'") from e


# General settings
def get_debug() -> bool:
    return _settings.get("debug", False)  # Still using default for non-critical debug


# Weather settings
def get_latitude() -> float:
    return float(get_value("weather/latitude"))


def get_longitude() -> float:
    return float(get_value("weather/longitude"))


def get_exclude() -> str:
    return get_value("weather/exclude")


def get_units() -> str:
    return get_value("weather/units")


def get_language() -> str:
    return get_value("weather/language")


def get_weather_request_interval() -> int:
    return get_value("weather/weather_request_interval")


def get_api_key() -> str:
    return get_value("weather/api_key")


def get_effects() -> bool:
    return get_value("weather/effects")


# Display settings
def get_display_height() -> int:
    return get_value("display/display_height")


def get_display_width() -> int:
    return get_value("display/display_width")


def get_target_fps() -> int:
    return get_value("display/target_fps")


def get_effects_display() -> bool:
    return get_value("display/effects")


def get_pin() -> int:
    return get_value("display/pin")


def get_target_frequency() -> int:
    return get_value("display/target_frequency")


def get_dma() -> int:
    return get_value("display/dma")


def get_strip_type() -> int:
    return get_value("display/strip_type")


def get_inverted() -> bool:
    return get_value("display/inverted")


def get_change_brightness() -> bool:
    return get_value("display/change_brightness")


def get_channel() -> int:
    return get_value("display/channel")


def get_brightness_day() -> int:
    return get_value("display/brightness")


def get_brightness_night() -> int:
    return get_value("display/brightness_night")


def switch_brightness() -> bool:
    return get_value("display/switch_brightness")


# Network settings
def get_port() -> int:
    return get_value("network/port")
