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


# Clock settings
class Clock:
    _instance = None

    _show: bool
    _time_format: str
    _show_seconds: bool
    _offset_x: int
    _offset_y: int
    _offset_delta: int

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Cache the values
            cls._instance._show = get_value("clock/show")
            cls._instance._time_format = get_value("clock/time_format")
            cls._instance._show_seconds = get_value("clock/show_seconds")
            cls._instance._offset_x = get_value("clock/offset_x")
            cls._instance._offset_y = get_value("clock/offset_y")
            cls._instance._offset_delta = get_value("clock/offset_delta")
        return cls._instance

    def show_clock(self) -> bool:
        return self._show

    def get_time_format(self) -> str:
        return self._time_format

    def show_seconds(self) -> bool:
        return self._show_seconds

    def get_offset_x(self) -> int:
        return self._offset_x

    def get_offset_y(self) -> int:
        return self._offset_y

    def get_offset_delta(self) -> int:
        return self._offset_delta


# Weather settings
class Weather:
    _instance = None

    _show_icon: bool
    _show_temp: bool
    _effects: bool
    _latitude: float
    _longitude: float
    _exclude: str
    _units: str
    _language: str
    _request_interval: int
    _api_key: str
    _offset_x: int
    _offset_y: int
    _offset_delta: int
    _offset_between: int
    _swap_icon_temp: bool

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Cache the values
            cls._instance._show_icon = get_value("weather/show_icon")
            cls._instance._show_temp = get_value("weather/show_temp")
            cls._instance._effects = get_value("weather/effects")
            cls._instance._latitude = float(get_value("weather/latitude"))
            cls._instance._longitude = float(get_value("weather/longitude"))
            cls._instance._exclude = get_value("weather/exclude")
            cls._instance._units = get_value("weather/units")
            cls._instance._language = get_value("weather/language")
            cls._instance._request_interval = get_value("weather/request_interval")
            cls._instance._api_key = get_value("weather/api_key")
            cls._instance._offset_x = get_value("weather/offset_x")
            cls._instance._offset_y = get_value("weather/offset_y")
            cls._instance._offset_delta = get_value("weather/offset_delta")
            cls._instance._offset_between = get_value("weather/offset_between")
            cls._instance._swap_icon_temp = get_value("weather/swap_icon_temp")
        return cls._instance

    def show_icon(self) -> bool:
        return self._show_icon

    def show_temp(self) -> bool:
        return self._show_temp

    def get_effects(self) -> bool:
        return self._effects

    def get_latitude(self) -> float:
        return self._latitude

    def get_longitude(self) -> float:
        return self._longitude

    def get_excluded(self) -> str:
        return self._exclude

    def get_units(self) -> str:
        return self._units

    def get_language(self) -> str:
        return self._language

    def get_request_interval(self) -> int:
        return self._request_interval

    def get_api_key(self) -> str:
        return self._api_key

    def get_offset_x(self) -> int:
        return self._offset_x

    def get_offset_y(self) -> int:
        return self._offset_y

    def get_offset_delta(self) -> int:
        return self._offset_delta

    def get_offset_between(self) -> int:
        return self._offset_between

    def swap_icon_temp(self) -> bool:
        return self._swap_icon_temp


# Display settings
class Display:
    _instance = None

    _height: int
    _width: int
    _target_fps: int
    _content_refresh_rate: int
    _effects: bool
    _pin: int
    _target_frequency: int
    _dma: int
    _strip_type: int
    _inverted: bool
    _change_brightness: bool
    _channel: int
    _brightness_day: int
    _brightness_night: int
    _switch_brightness: bool

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Cache the values once during the first instantiation
            cls._instance._height = get_value("display/height")
            cls._instance._width = get_value("display/width")
            cls._instance._target_fps = get_value("display/target_fps")
            cls._instance._content_refresh_rate = get_value(
                "display/content_refresh_rate"
            )
            cls._instance._effects = get_value("display/effects")
            cls._instance._pin = get_value("display/pin")
            cls._instance._target_frequency = get_value("display/target_frequency")
            cls._instance._dma = get_value("display/dma")
            cls._instance._strip_type = get_value("display/strip_type")
            cls._instance._inverted = get_value("display/inverted")
            cls._instance._change_brightness = get_value("display/change_brightness")
            cls._instance._channel = get_value("display/channel")
            cls._instance._brightness_day = get_value("display/brightness_day")
            cls._instance._brightness_night = get_value("display/brightness_night")
            cls._instance._switch_brightness = get_value("display/change_brightness")
        return cls._instance

    def get_height(self) -> int:
        return self._height

    def get_width(self) -> int:
        return self._width

    def get_target_fps(self) -> int:
        return self._target_fps

    def get_content_refresh_rate(self) -> int:
        return self._content_refresh_rate

    def get_effects_display(self) -> bool:
        return self._effects

    def get_pin(self) -> int:
        return self._pin

    def get_target_frequency(self) -> int:
        return self._target_frequency

    def get_dma(self) -> int:
        return self._dma

    def get_strip_type(self) -> int:
        return self._strip_type

    def get_inverted(self) -> bool:
        return self._inverted

    def get_change_brightness(self) -> bool:
        return self._change_brightness

    def get_channel(self) -> int:
        return self._channel

    def get_brightness_day(self) -> int:
        return self._brightness_day

    def get_brightness_night(self) -> int:
        return self._brightness_night

    def switch_brightness(self) -> bool:
        return self._switch_brightness


# Resources settings
class Resources:
    _instance = None

    _path: str

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Cache the values
            cls._instance._path = get_value("resources/path")
        return cls._instance

    def get_path(self) -> str:
        return self._path


# Network settings
class Network:
    _instance = None

    _api_port: int

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Cache the values
            cls._instance._api_port = get_value("network/api_port")
        return cls._instance

    def get_api_port(self) -> int:
        return self._api_port


# Logging settings
class Logging:
    _instance = None

    _level: str
    _path: str
    _to_file: bool
    _to_console: bool
    _format: str
    _file_timestamp: str
    _max_size: int
    _max_backups: int

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Cache the values
            cls._instance._level = get_value("logging/level")
            cls._instance._path = get_value("logging/path")
            cls._instance._to_file = get_value("logging/to_file")
            cls._instance._to_console = get_value("logging/to_console")
            cls._instance._format = get_value("logging/format")
            cls._instance._file_timestamp = get_value("logging/file_timestamp")
            cls._instance._max_size = get_value("logging/max_size")
            cls._instance._max_backups = get_value("logging/max_backups")
        return cls._instance

    def get_level(self) -> str:
        return self._level.upper()

    def get_path(self) -> str:
        return self._path

    def to_file(self) -> bool:
        return self._to_file

    def to_console(self) -> bool:
        return self._to_console

    def get_format(self) -> str:
        return self._format

    def get_file_timestamp(self) -> str:
        return self._file_timestamp

    def get_max_size(self) -> int:
        return self._max_size

    def get_max_backups(self) -> int:
        return self._max_backups


# Debug settings
class Debug:
    _instance = None

    _show_segments: bool

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Cache the values
            cls._instance._show_segments = get_value("debug/show_segments")
        return cls._instance

    def show_segments(self) -> bool:
        return self._show_segments
