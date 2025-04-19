from flask import Flask, jsonify, request
from weather_service import WeatherService
from models import db
import os

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///weather.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to Weather App API",
        "endpoints": {
            "current_weather": "/weather/current?city=<city>&country=<country>",
            "forecast": "/weather/forecast?city=<city>&country=<country>",
            "historical": "/weather/historical?city=<city>&country=<country>&days=<days>"
        }
    })

@app.route('/weather/current')
def get_current_weather():
    city = request.args.get('city', 'London')
    country = request.args.get('country', 'UK')
    
    weather_data = WeatherService.get_current_weather(city, country)
    if weather_data:
        return jsonify(WeatherService.parse_weather_data(weather_data))
    return jsonify({"error": "Could not fetch weather data"}), 500

@app.route('/weather/forecast')
def get_forecast():
    city = request.args.get('city', 'London')
    country = request.args.get('country', 'UK')
    
    forecast_data = WeatherService.get_weather_forecast(city, country)
    if forecast_data:
        return jsonify(forecast_data)
    return jsonify({"error": "Could not fetch forecast data"}), 500

@app.route('/weather/historical')
def get_historical():
    city = request.args.get('city', 'London')
    country = request.args.get('country', 'UK')
    days = int(request.args.get('days', 7))
    
    historical_data = WeatherService.get_historical_data(city, country, days)
    if historical_data:
        return jsonify([{
            'city': data.city,
            'country': data.country,
            'temperature': data.temperature,
            'timestamp': data.timestamp.isoformat()
        } for data in historical_data])
    return jsonify({"error": "Could not fetch historical data"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)