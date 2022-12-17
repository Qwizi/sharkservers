from typing import Optional, List

from pydantic import BaseModel

from app.roles.models import Role
from app.users.schemas import UserOut

RoleOut = Role.get_pydantic(exclude={"roles"})
RoleOutWithScopes = Role.get_pydantic()
RoleOutWithoutScopesAndUserRoles = Role.get_pydantic(exclude={"roles", "scopes"})


class StaffUserInRoles(BaseModel):
    id: int
    username: str
    avatar: str


class StaffRoles(BaseModel):
    id: int
    name: str
    color: str
    user_display_role: list[StaffUserInRoles]


class CreateRole(BaseModel):
    name: str
    color: str
    is_staff: bool = False
    scopes: Optional[List[int]] = None
