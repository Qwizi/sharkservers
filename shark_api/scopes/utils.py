from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.ormar import paginate
from ormar import NoMatch

from shark_api.roles.models import Role
from shark_api.scopes.enums import ScopeEnum
from shark_api.scopes.exceptions import scope_not_found_exception
from shark_api.scopes.models import Scope
from shark_api.scopes.schemas import CreateScopeSchema

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
    },
    {
        "app_name": "threads",
        "value": "close",
        "description": "Close threads"
    },
    {
        "app_name": "threads",
        "value": "open",
        "description": "Open threads"
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


async def _get_scopes(params: Params, role_id: int = None) -> AbstractPage:
    if role_id:
        return await paginate(Scope.objects.select_related("roles").filter(roles__id=role_id), params)
    return await paginate(Scope.objects, params)


async def _get_scope(scope_id: int) -> Scope:
    try:
        scope = await Scope.objects.get(id=scope_id)
        return scope
    except NoMatch:
        raise scope_not_found_exception


async def _create_scope(scope_data: CreateScopeSchema) -> Scope:
    return await Scope.objects.create(**scope_data.dict())


async def _delete_scope(scope_id: int) -> Scope:
    try:
        scope = await Scope.objects.get(id=scope_id, protected=False)
        await scope.delete()
        return scope
    except NoMatch:
        raise scope_not_found_exception
