"""
Enums for auth module.

Enums:
- RedisAuthKeyEnum: The keys for the redis auth codes.
- AuthExceptionsDetailEnum: The detail messages for the auth exceptions.
- AuthEventsEnum: The events for the auth module.
"""
from enum import Enum


class RedisAuthKeyEnum(str, Enum):
    """Enum class representing the keys used in Redis for authentication purposes."""

    ACTIVATE_USER = "activate-user-code"
    RESET_PASSWORD = "reset-password-code"  # noqa: S105
    CHANGE_EMAIL = "change-email-code"


class AuthExceptionsDetailEnum(str, Enum):
    """Enum class that defines the detail messages for various authentication exceptions."""

    EMAIL_TAKEN = "Email is taken"
    USERNAME_TAKEN = "Username is taken"
    INVALID_CODE = "Invalid code"
    USER_ACTIVATED = "User is already activated"
    INVALID_CREDENTIALS = "Invalid credentials"
    TOKEN_EXPIRED = "Token has expired"  # noqa: S105
    INACTIVE_USER = "Inactive user"
    NOT_ADMIN_USER = "Not admin user"
    INCORRECT_USERNAME_PASSWORD = "Incorrect username or password"  # noqa: S105
    NO_PERMISSIONS = "Not enough permissions"
    USER_EXISTS = "Email or username already exists"


class AuthEventsEnum(str, Enum):
    """Enum class that defines the events for the auth module."""

    REGISTERED_PRE = "USER_REGISTERED_PRE"
    REGISTERED_POST = "USER_REGISTERED_POST"
    ACTIVATED_PRE = "USER_ACTIVATED_PRE"
    ACTIVATED_POST = "USER_ACTIVATED_POST"
    ACCESS_TOKEN_PRE = "ACCESS_TOKEN_PRE"  # noqa: S105
    ACCESS_TOKEN_POST = "ACCESS_TOKEN_POST"  # noqa: S105
    REFRESH_TOKEN_PRE = "REFRESH_TOKEN_PRE"  # noqa: S105
    REFRESH_TOKEN_POST = "REFRESH_TOKEN"  # noqa: S105
