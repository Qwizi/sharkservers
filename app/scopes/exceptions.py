from starlette import status
from starlette.exceptions import HTTPException

from app.scopes.enums import ScopesExceptionsDetailEnum


class ScopeNotFound(HTTPException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Scope not found"


scope_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=ScopesExceptionsDetailEnum.NOT_FOUND,
)
