from pydantic import BaseModel

from app.users.models import User

UserOut = User.get_pydantic(exclude={"password", "email"})


class UserIn(BaseModel):
    username: str
    email: str
    password: str
