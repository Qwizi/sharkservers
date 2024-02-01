"""Schemas for the roles module."""
from __future__ import annotations

from pydantic import BaseModel

from sharkservers.roles.models import Role

role_out = Role.get_pydantic(exclude={"scopes", "user_roles", "user_display_role"})
role_out_with_scopes = Role.get_pydantic(exclude={"user_roles", "user_display_role"})
role_out_without_scopes_and_user_roles = Role.get_pydantic(exclude={"roles", "scopes"})


class RoleOut(role_out):
    """RoleOut schema."""


class RoleOutWithScopes(role_out_with_scopes):
    """RoleOutWithScopes schema."""


class RoleOutWithoutScopesAndUserRoles(role_out_without_scopes_and_user_roles):
    """RoleOutWithoutScopesAndUserRoles schema."""


class StaffUserInRolesSchema(BaseModel):
    """StaffUserInRolesSchema schema."""

    id: int
    username: str
    avatar: str


class StaffRolesSchema(BaseModel):
    """StaffRolesSchema schema."""

    id: int
    name: str
    color: str
    user_display_role: list[StaffUserInRolesSchema]


class CreateRoleSchema(BaseModel):
    """CreateRoleSchema schema."""

    tag: str
    name: str
    color: str
    is_staff: bool = False
    scopes: list[int] | None = None


class UpdateRoleSchema(BaseModel):
    """UpdateRoleSchema schema."""

    tag: str | None
    name: str | None
    color: str | None
    is_staff: bool | None
    scopes: list[int] | None
