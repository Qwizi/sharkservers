from enum import Enum


class ProtectedDefaultRolesEnum(int, Enum):
    ADMIN = 1
    USER = 2
    BANNED = 3


class RedisKeyEnum(Enum):
    ACTIVATE_USER = "activate-user-code"


class AuthExceptionsDetailEnum(str, Enum):
    EMAIL_TAKEN = "Email is taken"
    USERNAME_TAKEN = "Username is taken"
    INVALID_CODE = "Invalid code"
    USER_ACTIVATED = "User is already activated"
    INVALID_CREDENTIALS = "Invalid credentials"
    INACTIVE_USER = "Inactive user"
    NOT_ADMIN_USER = "Not admin user"
    INCORRECT_USERNAME_PASSWORD = "Incorrect username or password"
    NO_PERMISSIONS = "Not enough permissions"
    USER_EXISTS = "Email or username already exists"


class AuthEventsEnum(str, Enum):
    REGISTERED_PRE = "USER_REGISTERED_PRE"
    REGISTERED_POST = "USER_REGISTERED_POST"
    ACTIVATED_PRE = "USER_ACTIVATED_PRE"
    ACTIVATED_POST = "USER_ACTIVATED_POST"
    ACCESS_TOKEN_PRE = "ACCESS_TOKEN_PRE"
    ACCESS_TOKEN_POST = "ACCESS_TOKEN_POST"
    REFRESH_TOKEN_PRE = "REFRESH_TOKEN_PRE"
    REFRESH_TOKEN_POST = "REFRESH_TOKEN"
