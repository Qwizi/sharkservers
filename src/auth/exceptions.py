from fastapi import HTTPException
from starlette import status

from .enums import AuthExceptionsDetailEnum

username_taken_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=AuthExceptionsDetailEnum.USERNAME_TAKEN,
)
email_taken_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail=AuthExceptionsDetailEnum.EMAIL_TAKEN
)
invalid_activation_code_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=AuthExceptionsDetailEnum.INVALID_CODE,
)
user_activated_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=AuthExceptionsDetailEnum.USER_ACTIVATED,
)
not_admin_user_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=AuthExceptionsDetailEnum.NOT_ADMIN_USER,
)
incorrect_username_password_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=AuthExceptionsDetailEnum.INCORRECT_USERNAME_PASSWORD,
)
no_permissions_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=AuthExceptionsDetailEnum.NO_PERMISSIONS,
)
invalid_credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=AuthExceptionsDetailEnum.INVALID_CREDENTIALS,
)
inactivate_user_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=AuthExceptionsDetailEnum.INACTIVE_USER,
)
user_exists_exception = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail=AuthExceptionsDetailEnum.USER_EXISTS,
)
invalid_activation_code_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=AuthExceptionsDetailEnum.INVALID_CODE,
)
