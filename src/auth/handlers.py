from fastapi_events.handlers.local import local_handler
from fastapi_events.typing import Event

from src.auth.enums import AuthEventsEnum, RedisAuthKeyEnum
from src.auth.services import CodeService
from src.logger import logger
#from src.services import email_service
from src.settings import get_settings

"""
Auth events handlers
"""


@local_handler.register(event_name=AuthEventsEnum.REGISTERED_POST)
async def create_activate_code_after_register(event: Event):
    settings = get_settings()
    event_name, payload = event
    user_id = int(payload.get("id"))
    email = payload.get("email")
    redis = payload.get("redis")
    is_activated = payload.get("is_activated")
    code_service = CodeService(redis=redis, key=RedisAuthKeyEnum.ACTIVATE_USER)
    code, _user_id = await code_service.create(data=user_id, code_len=5, expire=900)
    logger.info(f"Activation code - {code} for {user_id}")
    # send only if not testing
    #if not settings.TESTING:
    #    await email_service.send_activation_email(email=email, code=code)
