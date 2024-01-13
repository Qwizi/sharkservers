"""
Schemas for the auth module.

Schemas:
- UsernameRegex: The schema for the username regex.
- PasswordSchema: The schema for the password.
- RegisterUserSchema: The schema for registering a user.
- TokenDetailsSchema: The schema for the token details.
- TokenSchema: The schema for the tokens.
- TokenDataSchema: The schema for the token data.
- RefreshTokenSchema: The schema for the refresh token.
- ActivateUserCodeSchema: The schema for the activation code.
- ResendActivationCodeSchema: The schema for resending the activation code.
- UserActivatedSchema: The schema for the user activated.
- EmailConfirmSchema: The schema for the email confirmation.
- ResetPasswordSchema: The schema for resetting the password.
- SteamAuthSchema: The schema for the steam auth.
"""
from __future__ import annotations

import datetime

from pydantic import BaseModel, EmailStr, Field, validator


class UsernameRegex(BaseModel):
    """Schema for the username regex."""

    username: str = Field(
        min_length=3,
        max_length=32,
        regex=r"^[a-zA-Z0-9_-]+$",
        strip_whitespace=True,
        default="username",
    )


class PasswordSchema(BaseModel):
    """Schema for validating password fields."""

    password: str = Field(min_length=8, max_length=255)
    password2: str = Field(min_length=8, max_length=255)

    @validator("password2")
    def passwords_match(cls, value, values, **kwargs) -> None:  # noqa: ANN001, N805, ARG002, ANN003
        """
        Check if the 'password2' field matches the 'password' field.

        Raises
        ------
            ValueError: If the passwords do not match.
        """
        if "password" in values and value != values["password"]:
            msg = "Passwords do not match"
            raise ValueError(msg)


class RegisterUserSchema(UsernameRegex, PasswordSchema):
    """Schema for registering a user."""

    email: EmailStr


class TokenDetailsSchema(BaseModel):
    """Schema for the token details."""

    token: str
    token_type: str
    exp: datetime.datetime


class TokenSchema(BaseModel):
    """Schema for the tokens."""

    access_token: TokenDetailsSchema
    refresh_token: TokenDetailsSchema


class TokenDataSchema(BaseModel):
    """Schema for the token data."""

    user_id: int | None = None
    secret: str
    scopes: list[str] = []
    session_id: str | None


class RefreshTokenSchema(BaseModel):
    """Schema for the refresh token."""

    refresh_token: str


class ActivateUserCodeSchema(BaseModel):
    """Schema for the activation code."""

    code: str = Field(max_length=5)


class ResendActivationCodeSchema(BaseModel):
    """Schema for resending the activation code."""

    email: EmailStr


class UserActivatedSchema(BaseModel):
    """Schema for the user activated."""

    id: int
    is_activated: bool


class EmailConfirmSchema(BaseModel):
    """Schema for the email confirmation."""

    old_email: EmailStr
    new_email: EmailStr
    is_confirmed: bool


class ResetPasswordSchema(ActivateUserCodeSchema, PasswordSchema):
    """Schema for resetting the password."""


class SteamAuthSchema(BaseModel):
    """Schema for the steam auth."""

    openid_ns: str
    openid_mode: str
    openid_op_endpoint: str
    openid_claimed_id: str
    openid_identity: str
    openid_return_to: str
    openid_response_nonce: str
    openid_assoc_handle: str
    openid_signed: str
    openid_sig: str
