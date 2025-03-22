import threading
import logging
import argparse
from weather_monitor import WeatherMonitor
from telegram_notifier import TelegramNotifier
import config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Weather Alert System')
    parser.add_argument('--city', default=config.CITY, 
                       help='City to monitor weather (default: from config)')
    parser.add_argument('--units', default=config.UNITS, choices=['metric', 'imperial'],
                       help='Temperature units (default: from config)')
    parser.add_argument('--interval', type=int, default=config.UPDATE_INTERVAL,
                       help='Update interval in seconds (default: from config)')
    args = parser.parse_args()
    
    logger.info("Starting Weather Alert System...")
    logger.info(f"Monitoring weather for {args.city} in {args.units} units")
    logger.info(f"Update interval: {args.interval} seconds")
    
    # Initialize the notification system (subscribes to events)
    telegram_notifier = TelegramNotifier()
    
    # Initialize and start the weather monitor in a separate thread
    monitor = WeatherMonitor(city=args.city, units=args.units)
    monitor_thread = threading.Thread(
        target=monitor.monitor_weather,
        args=(args.interval,),
        daemon=True
    )
    
    try:
        # Start the monitoring thread
        monitor_thread.start()
        
        # Keep the main thread running
        monitor_thread.join()
    except KeyboardInterrupt:
        logger.info("Shutting down Weather Alert System...")
    except Exception as e:
        logger.error(f"Error in main thread: {e}")

if __name__ == "__main__":
    main()