from asyncpg import UniqueViolationError
from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext import ormar
from fastapi_pagination.ext.ormar import paginate
from ormar import or_, and_, NoMatch

from app.roles.enums import ProtectedDefaultRolesEnum
from app.roles.exceptions import role_not_found_exception, role_exists_exception, role_protected_exception
from app.roles.models import Role
from app.roles.schemas import RoleOut, CreateRoleSchema
from app.scopes.models import Scope


async def get_admin_role_scopes():
    return await Scope.objects.all()


async def get_user_role_scopes():
    return await Scope.objects.filter(
        or_(
            and_(app_name="users", value="me"),
            and_(app_name="users", value="me:username"),
            and_(app_name="users", value="me:password"),
            and_(app_name="users", value="me:display-role"),
            and_(app_name="threads", value="create"),
            and_(app_name="posts", value="create"),
        )
    ).all()


async def create_default_roles():
    admin_role_id = 1
    user_role_id = 2
    banned_role_id = 3
    admin_role, created = await Role.objects.get_or_create(
        id=ProtectedDefaultRolesEnum.ADMIN.value,
        name="Admin",
        color="#C53030",
        is_staff=True
    )
    admin_scopes = await get_admin_role_scopes()
    for scope in admin_scopes:
        await admin_role.scopes.add(scope)
    user_role, _ = await Role.objects.get_or_create(
        id=ProtectedDefaultRolesEnum.USER.value,
        name="user",
        color="#99999"
    )
    user_scopes = await get_user_role_scopes()
    for scope in user_scopes:
        await user_role.scopes.add(scope)

    banned_role, _ = await Role.objects.get_or_create(
        id=ProtectedDefaultRolesEnum.BANNED.value,
        name="banned",
        color="#000000"
    )


async def _get_roles(params: Params) -> AbstractPage:
    return await paginate(Role.objects, params)


async def _get_staff_roles() -> dict:
    roles = await Role.objects.select_related(
        ["user_display_role"]).filter(
        is_staff=True
    ) \
        .all()
    # I need fix this
    return {
        "items": roles,
        "total": len(roles),
        "page": 1,
        "size": 50
    }


async def _get_role(role_id: int) -> Role:
    try:
        role = await Role.objects.select_related("scopes").get(id=role_id)
        return role
    except NoMatch as e:
        raise role_not_found_exception


async def _create_role(role_data: CreateRoleSchema) -> Role:
    scopes = None
    if role_data.scopes:
        scopes = await Scope.objects.filter(id__in=role_data.scopes).all()
    try:
        role = await Role.objects.create(
            name=role_data.name,
            color=role_data.color,
            is_staff=role_data.is_staff
        )
        if scopes:
            for scope in scopes:
                await role.scopes.add(scope)
        return role
    except UniqueViolationError as e:
        raise role_exists_exception


async def _delete_role(role_id: int) -> Role:
    if ProtectedDefaultRolesEnum.has_value(role_id):
        raise role_protected_exception
    role = await _get_role(role_id)
    await role.delete()
    return role
