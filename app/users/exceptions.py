from starlette import status
from starlette.exceptions import HTTPException


class UserNotFound(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "User not found"
