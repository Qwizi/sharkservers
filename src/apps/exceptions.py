# apps exceptions
from fastapi import status
from fastapi.exceptions import HTTPException
from src.apps.enums import AppsExceptionEnum


apps_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=AppsExceptionEnum.NOT_FOUND,
)
