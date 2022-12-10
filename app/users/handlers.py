from fastapi_events.handlers.local import local_handler
from fastapi_events.typing import Event

from app.auth.utils import create_activate_code
from app.db import get_redis
from app.logger import logger
from app.users.schemas import UserEvents


@local_handler.register(event_name=UserEvents.REGISTERED)
async def handle_user_register_event(event: Event):
    event_name, payload = event
    logger.info(f"User {payload['username']} register")


@local_handler.register(event_name=UserEvents.REGISTERED)
async def create_activate_code_after_register(event: Event):
    event_name, payload = event
    user_id = int(payload.get("id"))
    redis = payload.get("redis")
    code, _user_id = await create_activate_code(user_id=user_id, redis=redis)
    logger.info(f"Activation code - {code} for {user_id}")
