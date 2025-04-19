import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenWeatherMap API Configuration
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
OPENWEATHER_FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

# Default location (can be overridden)
DEFAULT_CITY = "London"
DEFAULT_COUNTRY = "UK"

# API Response Units
UNITS = "metric"  # Use metric units (Celsius) 