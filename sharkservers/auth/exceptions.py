"""
Exceptions for the auth module.

Exceptions:
----------
- username_taken_exception: Raised when a username is taken.
- email_taken_exception: Raised when an email is taken.
- invalid_activation_code_exception: Raised when an activation code is invalid.
- user_activated_exception: Raised when a user is already activated.
- not_admin_user_exception: Raised when a user is not an admin.
- incorrect_username_password_exception: Raised when the username or password is incorrect.
- no_permissions_exception: Raised when a user has no permissions.
- invalid_credentials_exception: Raised when the credentials are invalid.
- inactivate_user_exception: Raised when a user is inactive.
- user_exists_exception: Raised when a user exists.
- invalid_activation_code_exception: Raised when an activation code is invalid.
- token_expired_exception: Raised when a token is expired.
"""

from fastapi import HTTPException
from starlette import status

from .enums import AuthExceptionsDetailEnum

username_taken_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=AuthExceptionsDetailEnum.USERNAME_TAKEN,
)
email_taken_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=AuthExceptionsDetailEnum.EMAIL_TAKEN,
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
    status_code=status.HTTP_400_BAD_REQUEST,
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
token_expired_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=AuthExceptionsDetailEnum.TOKEN_EXPIRED,
)
