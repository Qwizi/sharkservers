from app.roles.models import Role
from app.scopes.enums import ScopeEnum
from app.scopes.models import Scope

"""
def create_scopes_for_application(app_name: str):
    scope_list = [(f"{app_name}:{e.value}", f"{e.value.capitalize()} {app_name}") for e in ScopeEnum]
    scope_dict = {}

    for scope in scope_list:
        if scope[0] not in scope_dict:
            scope_dict[scope[0]] = scope[1]

    return list(scope_dict.items())
"""


async def create_scopes_for_app(app_name: str, additional=None):
    for scope_enum in ScopeEnum:
        scope, created = await Scope.objects.get_or_create(
            app_name=app_name,
            value=scope_enum.value,
            description=f"{scope_enum.value} {app_name}s".capitalize()
        )
    if additional:
        for item in additional:
            additional_scope, additional_scope_created = await Scope.objects.get_or_create(
                app_name=item["app_name"],
                value=item["value"],
                description=item["description"]
            )


async def _create_scopes(applications, additional=None):
    for app in applications:
        await create_scopes_for_app(app, additional)


async def create_scopes():
    return await _create_scopes(["users", "roles", "scopes"], additional=[
        {
            "app_name": "users",
            "value": "me",
            "description": "Get logged users data"
        },
        {
            "app_name": "users",
            "value": "me:username",
            "description": "Update username"
        },
        {
            "app_name": "users",
            "value": "me:password",
            "description": "Update password"
        }
    ])


async def get_scopesv3(roles: list[Role]):
    scopes = []
    for role in roles:
        for scope in role.scopes:
            scope_str = scope.get_string()
            if scope_str not in scopes:
                scopes.append(scope.get_string())
    return scopes
