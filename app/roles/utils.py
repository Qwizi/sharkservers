from fastapi_pagination.ext import ormar
from ormar import or_, and_

from app.roles.models import Role
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
        id=admin_role_id,
        name="Admin",
        color="#C53030",
        is_staff=True
    )
    admin_scopes = await get_admin_role_scopes()
    for scope in admin_scopes:
        await admin_role.scopes.add(scope)
    user_role, _ = await Role.objects.get_or_create(
        id=user_role_id,
        name="user",
        color="#99999"
    )
    user_scopes = await get_user_role_scopes()
    for scope in user_scopes:
        await user_role.scopes.add(scope)

    banned_role, _ = await Role.objects.get_or_create(
        id=banned_role_id,
        name="banned",
        color="#000000"
    )
