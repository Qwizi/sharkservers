from starlette.exceptions import HTTPException


class UserNotFound(HTTPException):
    def __init__(self):
        self.status_code = 404
        self.detail = "User not found"
