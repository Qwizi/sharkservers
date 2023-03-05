from fastapi_events.handlers.local import local_handler
from fastapi_events.typing import Event

from src.enums import MainEventEnum
from src.logger import logger
from src.settings import get_settings

settings = get_settings()


def log_debug_event(event: Event):
    if settings.DEBUG:
        event_name, payload = event
        logger.debug(f"Event {event_name} with payload {payload}")


@local_handler.register(event_name="*")
async def handle_all_events_and_debug_log(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=MainEventEnum.INSTALL)
async def handle_install_event(event: Event):
    pass
