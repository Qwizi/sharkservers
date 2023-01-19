from enum import Enum
from typing import List

from pydantic import BaseModel, validator, constr, Field, EmailStr


class RegisterUserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    password2: str

    @validator('password2')
    def passwords_match(cls, value, values, **kwargs):
        if "password" in values and value != values["password"]:
            raise ValueError("Passwords do not match")


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    user_id: int | None = None
    secret: str
    scopes: list[str] = []


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class ActivateUserCodeSchema(BaseModel):
    code: str = Field(max_length=5)
