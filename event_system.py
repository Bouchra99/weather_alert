import logging

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EventBus:
    def __init__(self):
        self.subscribers = {}
    
    def subscribe(self, event_type, callback):
        """Register a callback function for a specific event type"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        logger.info(f"Subscribed callback to event: {event_type}")
        
    def publish(self, event_type, data):
        """Publish an event to all subscribers"""
        logger.info(f"Publishing event: {event_type}")
        
        if event_type not in self.subscribers:
            logger.warning(f"No subscribers for event: {event_type}")
            return
        
        # Notify all subscribers
        subscriber_count = len(self.subscribers[event_type])
        logger.info(f"Notifying {subscriber_count} subscribers for event: {event_type}")
        
        for callback in self.subscribers[event_type]:
            try:
                callback(data)
            except Exception as e:
                logger.error(f"Error in subscriber callback for event {event_type}: {e}")


event_bus = EventBus()