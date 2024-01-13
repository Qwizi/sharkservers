"""Module contains the enum classes used in the Sharkservers API for users."""  # noqa: EXE002
from enum import Enum


class UsersExceptionsDetailEnum(str, Enum):
    """Represents the detail of the exceptions raised in the Sharkservers API for users."""  # noqa: E501

    USER_NOT_FOUND = "User not found"
    USERNAME_NOT_AVAILABLE = "Username not available"
    INVALID_CURRENT_PASSWORD = "Invalid current password"  # noqa: S105
    CANNOT_CHANGE_DISPLAY_ROLE = (
        "U cannot change your display role if u don't have this role"
    )
    USER_NOT_BANNED = "User not banned"
    USER_ALREADY_BANNED = "User already banned"
    USER_EMAIL_IS_THE_SAME = "Email is the same"


class UsersEventsEnum(str, Enum):
    """Represents the events raised in the Sharkservers API for users."""

    GET_ALL_PRE = "USERS_GET_ALL_PRE"
    GET_ALL_POST = "USERS_GET_ALL_POST"
    GET_ONE_PRE = "USERS_GET_ONE_PRE"
    GET_ONE_POST = "USERS_GET_ONE_POST"
    ME_PRE = "USERS_ME_PRE"
    ME_POST = "USERS_ME_POST"
    CHANGE_USERNAME_PRE = "USERS_CHANGE_USERNAME_PRE"
    CHANGE_USERNAME_POST = "USERS_CHANGE_USERNAME_POST"
    CHANGE_PASSWORD_PRE = "USERS_CHANGE_PASSWORD_PRE"  # noqa: S105
    CHANGE_PASSWORD_POST = "USERS_CHANGE_PASSWORD_POST"  # noqa: S105
    CHANGE_DISPLAY_ROLE_PRE = "USERS_CHANGE_DISPLAY_ROLE_PRE"
    CHANGE_DISPLAY_ROLE_POST = "USERS_CHANGE_DISPLAY_ROLE_POST"
    GET_LAST_LOGGED_PRE = "USERS_GET_LAST_LOGGED_PRE"
    GET_LAST_LOGGED_POST = "USERS_GET_LAST_LOGGED_POST"
    GET_ONLINE_PRE = "USERS_GET_ONLINE_PRE"
    GET_ONLINE_POST = "USERS_GET_ONLINE_POST"


class UsersAdminEventsEnum(str, Enum):
    """Represents the events raised in the Sharkservers API for users."""

    GET_ALL = "USERS_ADMIN_GET_ALL"
    GET_ONE = "USERS_ADMIN_GET_ONE"
    CREATE = "USERS_ADMIN_CREATE"
    DELETE = "USERS_ADMIN_DELETE"
