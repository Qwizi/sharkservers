from starlette.exceptions import HTTPException


class UsernameIsTaken(HTTPException):
    def __init__(self):
        self.status_code = 401
        self.detail = "Username is taken"


class EmailIsTaken(HTTPException):
    def __init__(self):
        self.status_code = 401
        self.detail = "Email is taken"
