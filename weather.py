import requests

import settings

BASE_URL = "https://api.openweathermap.org/data/3.0/onecall"
TIMEOUT = 10


class Weather:
    def __init__(self, weather_data: dict):
        self.id = weather_data.get("id")
        self.main = weather_data.get("main")
        self.description = weather_data.get("description")
        self.icon = weather_data.get("icon")

    def __repr__(self):
        return f"Weather(id={self.id}, main='{self.main}', description='{self.description}', icon='{self.icon}')"


class CurrentWeather:
    def __init__(self, current_data: dict):
        self.dt = current_data.get("dt")
        self.sunrise = current_data.get("sunrise")
        self.sunset = current_data.get("sunset")
        self.temp = current_data.get("temp")
        self.feels_like = current_data.get("feels_like")
        self.pressure = current_data.get("pressure")
        self.humidity = current_data.get("humidity")
        self.dew_point = current_data.get("dew_point")
        self.uvi = current_data.get("uvi")
        self.clouds = current_data.get("clouds")
        self.visibility = current_data.get("visibility")
        self.wind_speed = current_data.get("wind_speed")
        self.wind_deg = current_data.get("wind_deg")
        self.weather = [Weather(weather) for weather in current_data.get("weather", [])]

    def __repr__(self):
        return (
            f"CurrentWeather(dt={self.dt}, sunrise={self.sunrise}, sunset={self.sunset}, temp={self.temp}, "
            f"feels_like={self.feels_like}, pressure={self.pressure}, humidity={self.humidity}, "
            f"dew_point={self.dew_point}, uvi={self.uvi}, clouds={self.clouds}, visibility={self.visibility}, "
            f"wind_speed={self.wind_speed}, wind_deg={self.wind_deg}, weather={self.weather})"
        )


class WeatherData:
    def __init__(self, data: dict):
        self.lat = data.get("lat")
        self.lon = data.get("lon")
        self.timezone = data.get("timezone")
        self.timezone_offset = data.get("timezone_offset")
        self.current = CurrentWeather(data.get("current", {}))

    def __repr__(self):
        return (
            f"WeatherData(lat={self.lat}, lon={self.lon}, timezone='{self.timezone}', "
            f"timezone_offset={self.timezone_offset}, current={self.current})"
        )


def call_api(params: dict) -> dict:
    response = requests.get(BASE_URL, params=params, timeout=TIMEOUT)
    if response.status_code == 200:
        return response.json()
    raise requests.exceptions.RequestException("API call failed")


def get_weather() -> WeatherData:
    parameter = {
        "lat": settings.get_latitude(),
        "lon": settings.get_longitude(),
        "exclude": settings.get_exclude(),
        "units": settings.get_units(),
        "lang": settings.get_language(),
        "appid": settings.get_api_key(),
    }

    data = call_api(parameter)
    return WeatherData(data)


if __name__ == "__main__":
    get_weather()
