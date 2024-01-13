# chat exceptions
from fastapi import status
from fastapi.exceptions import HTTPException
from sharkservers.chat.enums import ChatExceptionEnum

chat_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=ChatExceptionEnum.NOT_FOUND,
)
