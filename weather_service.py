import requests
from datetime import datetime
from config import (
    OPENWEATHER_API_KEY,
    OPENWEATHER_BASE_URL,
    OPENWEATHER_FORECAST_URL,
    UNITS
)
from models import db, WeatherData

class WeatherService:
    @staticmethod
    def get_current_weather(city, country):
        """
        Get current weather data for a specific city and store it in the database
        """
        try:
            params = {
                'q': f'{city},{country}',
                'appid': OPENWEATHER_API_KEY,
                'units': UNITS
            }
            response = requests.get(OPENWEATHER_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Store the data in the database
            weather_data = WeatherData(
                city=city,
                country=country,
                temperature=data['main']['temp'],
                feels_like=data['main']['feels_like'],
                humidity=data['main']['humidity'],
                pressure=data['main']['pressure'],
                wind_speed=data['wind']['speed'],
                description=data['weather'][0]['description']
            )
            
            db.session.add(weather_data)
            db.session.commit()
            
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
        except Exception as e:
            print(f"Error storing weather data: {e}")
            db.session.rollback()
            return None

    @staticmethod
    def get_weather_forecast(city, country):
        """
        Get 5-day weather forecast for a specific city
        """
        try:
            params = {
                'q': f'{city},{country}',
                'appid': OPENWEATHER_API_KEY,
                'units': UNITS
            }
            response = requests.get(OPENWEATHER_FORECAST_URL, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching forecast data: {e}")
            return None

    @staticmethod
    def get_historical_data(city, country, days=7):
        """
        Get historical weather data from the database
        """
        try:
            return WeatherData.query.filter_by(
                city=city,
                country=country
            ).order_by(WeatherData.timestamp.desc()).limit(days).all()
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return None

    @staticmethod
    def parse_weather_data(data):
        """
        Parse and format weather data
        """
        if not data:
            return None

        try:
            return {
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'city': data['name'],
                'country': data['sys']['country']
            }
        except KeyError as e:
            print(f"Error parsing weather data: {e}")
            return None 