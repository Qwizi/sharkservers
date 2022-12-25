from typing import Optional, List

from pydantic import BaseModel

from shark_api.roles.models import Role
from shark_api.users.schemas import UserOut

RoleOut = Role.get_pydantic(exclude={"roles"})
RoleOutWithScopes = Role.get_pydantic()
RoleOutWithoutScopesAndUserRoles = Role.get_pydantic(exclude={"roles", "scopes"})


class StaffUserInRolesSchema(BaseModel):
    id: int
    username: str
    avatar: str


class StaffRolesSchema(BaseModel):
    id: int
    name: str
    color: str
    user_display_role: list[StaffUserInRolesSchema]


class CreateRoleSchema(BaseModel):
    name: str
    color: str
    is_staff: bool = False
    scopes: Optional[List[int]] = None
