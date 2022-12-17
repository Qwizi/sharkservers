from app.roles.models import Role
from app.scopes.enums import ScopeEnum
from app.scopes.models import Scope

ADDITIONAL_SCOPES = [
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
    },
    {
        "app_name": "users",
        "value": "me:display-role",
        "description": "Change display role"
    }
]


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
    return await _create_scopes([
        "users",
        "roles",
        "scopes",
        "steamprofile",
        "categories",
        "tags",
        "threads",
        "posts"
    ], additional=ADDITIONAL_SCOPES)


async def get_scopesv3(roles: list[Role]):
    scopes = []
    for role in roles:
        for scope in role.scopes:
            scope_str = scope.get_string()
            if scope_str not in scopes:
                scopes.append(scope.get_string())
    return scopes
