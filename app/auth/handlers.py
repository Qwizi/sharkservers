from fastapi_events.handlers.local import local_handler
from fastapi_events.typing import Event

from app.auth.enums import AuthEventsEnum
from app.auth.utils import create_activate_code
from app.logger import logger


def log_debug_event(event: Event):
    event_name, payload = event
    logger.debug(f"Event {event_name} with payload {payload}")


@local_handler.register(event_name=AuthEventsEnum.REGISTERED_PRE)
async def handle_auth_event_registered_pre(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=AuthEventsEnum.REGISTERED_POST)
async def handle_auth_event_registered_post(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=AuthEventsEnum.ACTIVATED_PRE)
async def handle_auth_event_activated_pre(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=AuthEventsEnum.ACTIVATED_POST)
async def handle_auth_event_activated_post(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=AuthEventsEnum.ACCESS_TOKEN_PRE)
async def handle_auth_event_access_token_pre(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=AuthEventsEnum.ACCESS_TOKEN_POST)
async def handle_auth_event_access_token_post(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=AuthEventsEnum.REFRESH_TOKEN_PRE)
async def handle_auth_event_refresh_token_pre(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=AuthEventsEnum.REFRESH_TOKEN_POST)
async def handle_auth_event_refresh_token_post(event: Event):
    log_debug_event(event)


@local_handler.register(event_name=AuthEventsEnum.REGISTERED_POST)
async def create_activate_code_after_register(event: Event):
    event_name, payload = event
    user_id = int(payload.get("id"))
    redis = payload.get("redis")
    code, _user_id = await create_activate_code(user_id=user_id, redis=redis)
    logger.info(f"Activation code - {code} for {user_id}")
