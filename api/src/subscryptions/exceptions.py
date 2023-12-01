from fastapi import HTTPException, status

from src.subscryptions.enums import UserSubscryptionExceptionsDetailEnum


subscryption_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=UserSubscryptionExceptionsDetailEnum.SUBSCRYPTION_NOT_FOUND,
)
