import time 
import random 
from event_system import event_bus
import logging
import config
import requests

logging.basicConfig(
    level= logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WeatherMonitor : 
    def __init__(self, city = config.CITY, units = config.UNITS):
        self.city = city 
        self.units = units 
        self.api_key = config.OPENWEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.last_data = None

    def get_weather_data(self): 
        """Fetch weather data from OpenWeather API"""
        params = {
            'q': self.city,
            'appid': self.api_key,
            'units': self.units
        }
        try : 
            response = requests.get(self.base_url, params=params)
            response.raise_for_status() # Raise exceptions for Http errors

            data = response.json()

            weather_data = {
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'weather_condition': data['weather'][0]['main'],
                'weather_description': data['weather'][0]['description'],
                'city': data['name'],
                'timestamp': time.time()
            }

            return weather_data
        except  requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather data: {e}")
            return None



    def monitor_weather(self, interval=config.UPDATE_INTERVAL) :
        while True : 
            weather_data = self.get_weather_data()

            if weather_data  : 
                event_bus.publish('weather_update', weather_data)

            if weather_data['temperature'] > 5:
                event_bus.publish('high_temperature_alert', weather_data)
            
            if weather_data['wind_speed'] > 5:
                event_bus.publish('high_wind_alert', weather_data)
                
            if weather_data['humidity'] > 80:
                event_bus.publish('high_humidity_alert', weather_data)
            
            if self.last_data and self.last_data['weather_condition'] != weather_data['weather_condition']:
                    event_bus.publish('weather_condition_change', {
                        'previous': self.last_data['weather_condition'],
                        'current': weather_data['weather_condition'],
                        'description': weather_data['weather_description'],
                        'city': weather_data['city'],
                        'timestamp': weather_data['timestamp']
                    })
                
                
            self.last_data = weather_data

            time.sleep(interval)