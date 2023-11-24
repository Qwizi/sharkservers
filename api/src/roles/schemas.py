from typing import Optional, List

from pydantic import BaseModel

from src.roles.models import Role

role_out = Role.get_pydantic(exclude={"scopes", "user_roles", "user_display_role"})
role_out_with_scopes = Role.get_pydantic(exclude={"user_roles", "user_display_role"})
role_out_without_scopes_and_user_roles = Role.get_pydantic(exclude={"roles", "scopes"})


class RoleOut(role_out):
    pass


class RoleOutWithScopes(role_out_with_scopes):
    pass


class RoleOutWithoutScopesAndUserRoles(role_out_without_scopes_and_user_roles):
    pass


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


class UpdateRoleSchema(BaseModel):
    name: Optional[str]
    color: Optional[str]
    is_staff: Optional[bool]
    scopes: Optional[List[int]]
