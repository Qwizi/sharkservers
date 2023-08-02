from typing import Optional

from pydantic import BaseModel, validator, EmailStr

from src.auth.schemas import UsernameRegex
from src.users.models import User

UserOut = User.get_pydantic(
    exclude={"password", "email", "secret_salt", "apps", "players", "banned_user", "banned_by", "roles", "password_reset_token"})
UserOutWithEmail = User.get_pydantic(exclude={"password", "secret_salt", "apps", "players", "password_reset_token"})


class ChangeUsernameSchema(UsernameRegex):
    pass


class SuccessChangeUsernameSchema(BaseModel):
    old_username: str
    new_username: str


class ChangePasswordSchema(BaseModel):
    current_password: str
    new_password: str
    new_password2: str

    @validator("new_password2")
    def passwords_match(cls, value, values, **kwargs):
        if "new_password" in values and value != values["new_password"]:
            raise ValueError("Passwords do not match")


class ChangeEmailSchema(BaseModel):
    email: EmailStr


class ChangeDisplayRoleSchema(BaseModel):
    role_id: int


class SuccessChangeDisplayRoleSchema(BaseModel):
    old_role_id: int
    new_role_id: int


class CreateUserSchema(BaseModel):
    username: str
    email: str
    password: str
    is_activated: bool = False
    is_superuser: bool = False


class CreateAdminUserSchema(CreateUserSchema):
    is_admin: bool = True


class BanUserSchema(BaseModel):
    reason: str
    ban_time: int


class AdminUpdateUserSchema(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
    is_activated: Optional[bool]
    is_superuser: Optional[bool]
    avatar: Optional[str]
    roles: Optional[list[int]]
    display_role: Optional[int]
    secret_salt: Optional[str]
