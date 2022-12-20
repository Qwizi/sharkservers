from starlette import status
from starlette.exceptions import HTTPException

from app.roles.enums import RolesExceptionsDetailEnum

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
