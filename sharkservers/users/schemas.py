"""
Module contains the schema definitions for the users in the SharkServers API.

It includes Pydantic models for various user-related operations such as creating a user, changing username, changing password, etc.

The module also defines query parameters for filtering and ordering user data.

"""
from __future__ import annotations

from fastapi import Query
from pydantic import BaseModel, EmailStr, validator

from sharkservers.auth.schemas import UsernameRegex
from sharkservers.schemas import OrderQuery
from sharkservers.users.models import User, UserSession

user_out = User.get_pydantic(
    exclude={
        "password",
        "email",
        "secret_salt",
        "apps",
        "banned_user",
        "banned_by",
        "roles__scopes",
        "password_reset_token",
        "display_role__scopes",
    },
)
user_out_with_email = User.get_pydantic(
    exclude={"password", "secret_salt", "apps", "password_reset_token"},
)
user_session_out = UserSession.get_pydantic(exclude={"users_sessions"})


class UserSessionOut(user_session_out):
    """Represents the output schema for a user session."""


class UserOut(user_out):
    """Represents the output schema for a user."""


class UserOutWithEmail(user_out_with_email):
    """Represents the output schema for a user with email."""


class ChangeUsernameSchema(UsernameRegex):
    """
    Schema for changing the username.

    Attributes
    ----------
        new_username (str): The new username to be set.
    """

    new_username: str


class SuccessChangeUsernameSchema(BaseModel):
    """Schema for successful username change response."""

    old_username: str
    new_username: str


class ChangePasswordSchema(BaseModel):
    """
    Schema for changing password.

    Attributes
    ----------
        current_password (str): The current password.
        new_password (str): The new password.
        new_password2 (str): The confirmation of the new password.

    Raises
    ------
        ValueError: If the new_password2 does not match the new_password.
    """

    current_password: str
    new_password: str
    new_password2: str

    @validator("new_password2")
    def passwords_match(cls, value, values, **kwargs) -> None:  # noqa: ANN001, ANN003, ARG002, N805
        """Validate that the new_password2 matches the new_password."""
        if "new_password" in values and value != values["new_password"]:
            msg = "Passwords do not match"
            raise ValueError(msg)


class ChangeEmailSchema(BaseModel):
    """
    Schema for changing email.

    Attributes
    ----------
        email (str): The new email address.
    """

    email: EmailStr


class ChangeDisplayRoleSchema(BaseModel):
    """Schema for changing the display role of a user."""

    role_id: int


class SuccessChangeDisplayRoleSchema(BaseModel):
    """Schema for representing a successful change in display role."""

    old_role_id: int
    new_role_id: int


class CreateUserSchema(BaseModel):
    """Schema for creating a user."""

    username: str
    email: str
    password: str
    is_activated: bool = False
    is_superuser: bool = False


class CreateAdminUserSchema(CreateUserSchema):
    """Schema for creating an admin user."""

    is_admin: bool = True


class BanUserSchema(BaseModel):
    """Schema for banning a user."""

    reason: str
    ban_time: int


class AdminUpdateUserSchema(BaseModel):
    """Schema for updating a user."""

    username: str | None
    email: str | None
    password: str | None
    is_activated: bool | None
    is_superuser: bool | None
    avatar: str | None
    roles: list[int] | None
    display_role: int | None
    secret_salt: str | None


class UserQuery(OrderQuery):
    """Query parameters for filtering and ordering users."""

    username: str | None = Query(None, description="Username")
