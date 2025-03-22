import asyncio
from telegram import Bot
import logging 
from event_system import event_bus
import config 


logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TelegramNotifier : 

    def __init__(self):
        
        self.bot_token = config.TELEGRAM_BOT_TOKEN
        self.chat_id = config.TELEGRAM_CHAT_ID
        self.bot = Bot(token=self.bot_token)

        self.high_temp_alerted = False
        self.high_wind_alerted = False
        self.high_humidity_alerted = False
        
        event_bus.subscribe('weather_update', self.on_weather_update)
        event_bus.subscribe('high_temperature_alert', self.on_high_temperature)
        event_bus.subscribe('high_wind_alert', self.on_high_wind)
        event_bus.subscribe('high_humidity_alert', self.on_high_humidity)
        event_bus.subscribe('weather_condition_change', self.on_weather_change)

    
    async def send_message(self, message):
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=message, parse_mode='HTML')
            return True
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False
    
    def on_weather_update(self, data):
        """Handle regular weather updates - log only, no notification"""
        logger.info(f"Weather Update for {data['city']}: "
                   f"{data['temperature']}°{'F' if config.UNITS == 'imperial' else 'C'}, "
                   f"Humidity: {data['humidity']}%, "
                   f"Wind: {data['wind_speed']} {'mph' if config.UNITS == 'imperial' else 'km/h'}")
        
        # Reset alert flags if conditions return to normal
        if data['temperature'] <= 30 and self.high_temp_alerted:
            self.high_temp_alerted = False
            asyncio.run(self.send_message(
                f"✅ Temperature in {data['city']} has returned to normal levels: "
                f"{data['temperature']}°{'F' if config.UNITS == 'imperial' else 'C'}"
            ))
            
        if data['wind_speed'] <= 15 and self.high_wind_alerted:
            self.high_wind_alerted = False
            asyncio.run(self.send_message(
                f"✅ Wind speed in {data['city']} has returned to normal levels: "
                f"{data['wind_speed']} {'mph' if config.UNITS == 'imperial' else 'km/h'}"
            ))
            
        if data['humidity'] <= 80 and self.high_humidity_alerted:
            self.high_humidity_alerted = False
            asyncio.run(self.send_message(
                f"✅ Humidity in {data['city']} has returned to normal levels: {data['humidity']}%"
            ))
    
    def on_high_temperature(self, data):
        """Handle high temperature alerts"""
        if not self.high_temp_alerted:
            message = (
                f"⚠️ <b>HIGH TEMPERATURE ALERT</b> ⚠️\n\n"
                f"Temperature in {data['city']} is now {data['temperature']}°"
                f"{'F' if config.UNITS == 'imperial' else 'C'}!\n\n"
                f"• Feels like: {data['feels_like']}°"
                f"{'F' if config.UNITS == 'imperial' else 'C'}\n"
                f"• Current conditions: {data['weather_description']}\n\n"
            )
            asyncio.run(self.send_message(message))
            self.high_temp_alerted = True
    
    def on_high_wind(self, data):
        """Handle high wind alerts"""
        if not self.high_wind_alerted:
            message = (
                f"⚠️ <b>HIGH WIND ALERT</b> ⚠️\n\n"
                f"Wind speed in {data['city']} is now {data['wind_speed']} "
                f"{'mph' if config.UNITS == 'imperial' else 'km/h'}!\n\n"
                f"• Temperature: {data['temperature']}°"
                f"{'F' if config.UNITS == 'imperial' else 'C'}\n"
                f"• Current conditions: {data['weather_description']}\n\n"
            )
            asyncio.run(self.send_message(message))
            self.high_wind_alerted = True
    
    def on_high_humidity(self, data):
        """Handle high humidity alerts"""
        if not self.high_humidity_alerted:
            message = (
                f"⚠️ <b>HIGH HUMIDITY ALERT</b> ⚠️\n\n"
                f"Humidity in {data['city']} is now {data['humidity']}%!\n\n"
                f"• Temperature: {data['temperature']}°"
                f"{'F' if config.UNITS == 'imperial' else 'C'}\n"
                f"• Feels like: {data['feels_like']}°"
                f"{'F' if config.UNITS == 'imperial' else 'C'}\n"
                f"• Current conditions: {data['weather_description']}\n\n"
            )
            asyncio.run(self.send_message(message))
            self.high_humidity_alerted = True
    
    def on_weather_change(self, data):
        """Handle weather condition changes"""
        message = (
            f"🔄 <b>WEATHER CHANGE</b> 🔄\n\n"
            f"Weather in {data['city']} has changed from "
            f"<b>{data['previous']}</b> to <b>{data['current']}</b>.\n\n"
            f"Current conditions: {data['description']}"
        )
        asyncio.run(self.send_message(message))