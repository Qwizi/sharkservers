from fastapi import HTTPException

from src.servers.enums import ServerExceptionEnum

server_not_found_exception = HTTPException(
    detail=ServerExceptionEnum.NOT_FOUND, status_code=404
)
