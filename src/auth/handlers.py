from fastapi_events.handlers.local import local_handler
from fastapi_events.typing import Event

from src.auth.enums import AuthEventsEnum
from src.auth.utils import create_activate_code
from src.handlers import log_debug_event
from src.logger import logger
from src.services import email_service
from src.users.services import users_service

"""
Auth events handlers
"""


@local_handler.register(event_name=AuthEventsEnum.REGISTERED_POST)
async def create_activate_code_after_register(event: Event):
    event_name, payload = event
    user_id = int(payload.get("id"))
    user = await users_service.get_one(id=user_id)
    redis = payload.get("redis")
    code, _user_id = await create_activate_code(user_id=user_id, redis=redis)
    logger.info(f"Activation code - {code} for {user_id}")
    await email_service.send_activation_email(email=user.email, code=code)
