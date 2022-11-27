from starlette import status
from starlette.exceptions import HTTPException


class UsernameIsTaken(HTTPException):
    def __init__(self):
        self.status_code = 401
        self.detail = "Username is taken"


class EmailIsTaken(HTTPException):
    def __init__(self):
        self.status_code = 401
        self.detail = "Email is taken"


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

inactive_user_exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
invalid_username_password_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)
