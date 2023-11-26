from fastapi import HTTPException
from starlette import status

from src.users.enums import UsersExceptionsDetailEnum


class UserNotFound(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "User not found"


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
