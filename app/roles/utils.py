from app.roles.models import Role
from app.scopes.models import Scope


async def get_admin_role_scopes():
    return await Scope.objects.all()


async def get_user_role_scopes():
    return await Scope.objects.filter(app_name="users", value="me").all()


async def create_default_roles():
    admin_role_id = 1
    user_role_id = 2
    admin_role, created = await Role.objects.get_or_create(
        id=admin_role_id,
        name="Admin",
        color="#C53030"
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
