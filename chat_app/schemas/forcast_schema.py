from pydantic import BaseModel
from typing import Optional

class CurrentWeather(BaseModel):
    time: str
    interval: int
    temperature: float
    windspeed: float
    winddirection: int
    is_day: bool
    weathercode: int
    

class CurrentWeatherUnits(BaseModel):
    time:str
    interval: str
    temperature: str
    windspeed: str
    winddirection: str
    is_day: Optional[bool] = None
    weathercode: str



class Location(BaseModel):
    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: float
    current_weather_units: CurrentWeatherUnits
    current_weather: CurrentWeather
    
