from fastapi import HTTPException


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
