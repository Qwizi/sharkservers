from starlette.exceptions import HTTPException


class RoleScopeNotFound(HTTPException):
    def __init__(self):
        self.status_code = 401
        self.detail = "Scopes for this role not exists"


class ScopeNotFound(HTTPException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Scope not found"
