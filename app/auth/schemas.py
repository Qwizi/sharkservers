from enum import Enum
from typing import List

from pydantic import BaseModel, validator, constr, Field


class RegisterUser(BaseModel):
    username: str
    email: str
    password: str
    password2: str

    @validator('password2')
    def passwords_match(cls, value, values, **kwargs):
        if "password" in values and value != values["password"]:
            raise ValueError("Passwords do not match")


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None
    scopes: list[str] = []


class RefreshToken(BaseModel):
    refresh_token: str


class ActivateUserCode(BaseModel):
    code: str = Field(max_length=5)
