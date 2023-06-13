import datetime
from typing import Optional, List

from pydantic import BaseModel, validator

from src.players.schemas import SteamPlayer
from src.users.models import User

UserOut = User.get_pydantic(exclude={"password", "email", "secret_salt", "apps", "players", "last_login"})
UserOutWithEmail = User.get_pydantic(exclude={"password"})


class UserInSchema(BaseModel):
    username: str
    email: str
    password: str


class UserOutRoleSchema(BaseModel):
    id: int
    name: Optional[str] = None
    color: Optional[str] = None
    is_staff: Optional[bool] = None


class UserOut2Schema(BaseModel):
    id: int
    username: Optional[str] = None
    avatar: Optional[str] = None
    display_role: Optional[UserOutRoleSchema] = None
    roles: Optional[List[UserOutRoleSchema]] = None
    steamprofile: Optional[SteamPlayer] = None


class ChangeUsernameSchema(BaseModel):
    username: str


class ChangePasswordSchema(BaseModel):
    current_password: str
    new_password: str
    new_password2: str

    @validator("new_password2")
    def passwords_match(cls, value, values, **kwargs):
        if "new_password" in values and value != values["new_password"]:
            raise ValueError("Passwords do not match")


class ChangeDisplayRoleSchema(BaseModel):
    role_id: int


class CreateUserSchema(BaseModel):
    username: str
    email: str
    password: str
    display_role: Optional[int] = None
    roles: Optional[List[int]] = None
    is_activated: bool = True


class CreateAdminUserSchema(CreateUserSchema):
    is_admin: bool = True


class BanUserSchema(BaseModel):
    reason: str
    ban_time: int
