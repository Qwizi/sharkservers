"""Exceptions for scopes module."""  # noqa: EXE002
from starlette import status
from starlette.exceptions import HTTPException

from sharkservers.scopes.enums import ScopesExceptionsDetailEnum

scope_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=ScopesExceptionsDetailEnum.NOT_FOUND,
)
