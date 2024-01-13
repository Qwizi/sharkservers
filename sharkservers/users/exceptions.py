"""
This module contains custom exceptions related to user operations.

Exceptions:
----------
- user_not_found_exception: Raised when a user is not found.
- username_not_available_exception: Raised when a username is not available.
- invalid_current_password_exception: Raised when the current password is invalid.
- cannot_change_display_role_exception: Raised when a user tries to change their display role.
- user_already_banned_exception: Raised when a user is already banned.
- user_not_banned_exception: Raised when a user is not banned.
- user_email_is_the_same_exception: Raised when a user tries to change their email to the same email.
"""  # noqa: D404, E501, EXE002
from fastapi import HTTPException
from starlette import status

from sharkservers.users.enums import UsersExceptionsDetailEnum

user_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=UsersExceptionsDetailEnum.USER_NOT_FOUND,
)

username_not_available_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=UsersExceptionsDetailEnum.USERNAME_NOT_AVAILABLE,
)

invalid_current_password_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=UsersExceptionsDetailEnum.INVALID_CURRENT_PASSWORD,
)

cannot_change_display_role_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=UsersExceptionsDetailEnum.CANNOT_CHANGE_DISPLAY_ROLE,
)

user_already_banned_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=UsersExceptionsDetailEnum.USER_ALREADY_BANNED,
)

user_not_banned_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=UsersExceptionsDetailEnum.USER_NOT_BANNED,
)

user_email_is_the_same_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=UsersExceptionsDetailEnum.USER_EMAIL_IS_THE_SAME,
)
