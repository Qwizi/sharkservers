from enum import Enum
from typing import Optional

from aioredis import Redis
from fastapi_events.registry.payload_schema import registry as payload_schema
from pydantic import BaseModel, validator

from app.users.models import User


class UserEvents(Enum):
    REGISTERED = "USER_REGISTERED"
    ACTIVATED = "USER_ACTIVATED"
    ACCESS_TOKEN = "ACCESS_TOKEN"
    REFRESH_TOKEN = "REFRESH_TOKEN"


UserOut = User.get_pydantic(exclude={"password", "email"})
UserOutWithEmail = User.get_pydantic(exclude={"password"})


class UserIn(BaseModel):
    username: str
    email: str
    password: str


class ChangeUsername(BaseModel):
    username: str


class ChangePassword(BaseModel):
    current_password: str
    new_password: str
    new_password2: str

    @validator('new_password2')
    def passwords_match(cls, value, values, **kwargs):
        if "new_password" in values and value != values["new_password"]:
            raise ValueError("Passwords do not match")


class ChangeDisplayRole(BaseModel):
    role_id: int


@payload_schema.register(event_name=UserEvents.REGISTERED)
class RegisteredUserPayload(UserOut):
    redis: Optional[Redis]

    class Config:
        arbitrary_types_allowed = True
