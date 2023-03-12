from fastapi import HTTPException
from starlette import status


class SteamProfileNotFound(HTTPException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Steam profile not found"


class SteamProfileExists(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = "Steam profile exists"


class InvalidSteamid(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = "Invalid steamid"


player_not_found_exception = HTTPException(
    detail="Player not found", status_code=status.HTTP_404_NOT_FOUND
)
