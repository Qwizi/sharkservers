from starlette.exceptions import HTTPException


class RoleNotFound(HTTPException):
    def __init__(self):
        self.status_code = 401
        self.detail = "Role not found"


class RoleExists(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = "Role with this name already exists"
