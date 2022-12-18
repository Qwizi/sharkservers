from fastapi_events.typing import Event

from app.logger import logger


def log_debug_event(event: Event):
    event_name, payload = event
    logger.debug(f"Event {event_name} with payload {payload}")
