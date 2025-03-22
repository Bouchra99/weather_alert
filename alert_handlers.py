from event_system import event_bus

class AlertSystem : 
    def __init__(self):
        event_bus.subscribe('weather_update', self.on_weather_update)
        event_bus.subscribe('high_temperature_alert', self.on_high_temperature)
        event_bus.subscribe('high_wind_alert', self.on_high_wind)
        event_bus.subscribe('high_humidity_alert', self.on_high_humidity)

        # Track alert states to prevent duplicate alerts
        self.high_temp_alerted = False
        self.high_wind_alerted = False
        self.high_humidity_alerted = False

    def on_weather_update(self, data):
        """Handle regular weather updates"""
        print(f"\nWeather Update: {data['timestamp']}")
        print(f"Temperature: {data['temperature']:.1f}°C")
        print(f"Humidity: {data['humidity']:.1f}%")
        print(f"Wind Speed: {data['wind_speed']:.1f} mph")
        
        # Reset alert states if conditions return to normal
        if data['temperature'] <= 90 and self.high_temp_alerted:
            self.high_temp_alerted = False
            print("✓ Temperature has returned to normal levels")
            
        if data['wind_speed'] <= 15 and self.high_wind_alerted:
            self.high_wind_alerted = False
            print("✓ Wind speed has returned to normal levels")
            
        if data['humidity'] <= 80 and self.high_humidity_alerted:
            self.high_humidity_alerted = False
            print("✓ Humidity has returned to normal levels")
    
    def on_high_temperature(self, data):
        """Handle high temperature alerts"""
        if not self.high_temp_alerted:
            print(f"⚠️ ALERT: High temperature detected: {data['temperature']:.1f}°F!")
            print("   Recommend staying hydrated and avoiding outdoor activities")
            self.high_temp_alerted = True
    
    def on_high_wind(self, data):
        """Handle high wind alerts"""
        if not self.high_wind_alerted:
            print(f"⚠️ ALERT: High winds detected: {data['wind_speed']:.1f} mph!")
            print("   Recommend securing loose outdoor items")
            self.high_wind_alerted = True
    
    def on_high_humidity(self, data):
        """Handle high humidity alerts"""
        if not self.high_humidity_alerted:
            print(f"⚠️ ALERT: High humidity detected: {data['humidity']:.1f}%!")
            print("   Heat index may be higher than actual temperature")
            self.high_humidity_alerted = True