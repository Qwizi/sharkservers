from fastapi_events.handlers.local import local_handler
from fastapi_events.typing import Event

from src.auth.enums import AuthEventsEnum, RedisAuthKeyEnum
from src.auth.services import CodeService
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
    email = payload.get("email")
    redis = payload.get("redis")
    code_service = CodeService(redis=redis, key=RedisAuthKeyEnum.ACTIVATE_USER)
    # code, _user_id = await create_activate_code(user_id=user_id, redis=redis)
    code, _user_id = await code_service.create(data=user_id, code_len=5, expire=900)
    logger.info(f"Activation code - {code} for {user_id}")
    await email_service.send_activation_email(email=email, code=code)
