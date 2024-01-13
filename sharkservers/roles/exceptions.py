"""Exceptions for roles module."""

from fastapi import status
from fastapi.exceptions import HTTPException

from sharkservers.roles.enums import RolesExceptionsDetailEnum

role_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=RolesExceptionsDetailEnum.NOT_FOUND,
)

role_exists_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=RolesExceptionsDetailEnum.ALREADY_EXISTS,
)

role_protected_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=RolesExceptionsDetailEnum.PROTECTED,
)
