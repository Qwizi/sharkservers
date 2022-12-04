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
        }
    ])


async def get_scopes():
    scopes_dict = {}
    scopes = await Scope.objects.all()
    for scope in scopes:
        scope_tuple = scope.get_tuple()
        if scope_tuple[0] not in scopes_dict:
            scopes_dict[scope_tuple[0]] = scope_tuple[1]
    return scopes_dict


async def get_scopesv2():
    scopes = await Scope.objects.all()
    scopes_list = []
    for scope in scopes:
        scopes_list.append(scope.get_string())
    return scopes_list
