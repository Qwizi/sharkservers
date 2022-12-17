from fastapi import APIRouter, Depends, Security
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.ormar import paginate
from ormar import NoMatch

from app.auth.utils import get_admin_user
from app.scopes.exceptions import ScopeNotFound
from app.scopes.models import Scope
from app.scopes.schemas import ScopeOut, CreateScope
from app.users.models import User

router = APIRouter()


@router.get("", response_model=Page[ScopeOut])
async def admin_get_scopes(params: Params = Depends(),
                           user: User = Security(get_admin_user, scopes=["scopes:get_all"])):
    scopes = Scope.objects
    return await paginate(scopes, params)


@router.get("/{scope_id}", response_model=ScopeOut)
async def admin_get_scope(scope_id: int, user: User = Security(get_admin_user, scopes=["scopes:retrieve"])):
    try:
        scope = await Scope.objects.get(id=scope_id)
        return scope
    except NoMatch:
        raise ScopeNotFound()


@router.post("", response_model=ScopeOut)
async def admin_create_scope(scope_data: CreateScope, user: User = Security(get_admin_user, scopes=["scopes:create"])):
    scope = await Scope.objects.create(
        app_name=scope_data.app_name,
        value=scope_data.value,
        description=scope_data.description,
        protected=scope_data.protected
    )
    return scope


@router.delete("/{scope_id}", response_model=ScopeOut)
async def admin_delete_scope(scope_id: int, user: User = Security(get_admin_user, scopes=["scopes:delete"])):
    try:
        scope = await Scope.objects.get(id=scope_id, protected=False)
        await scope.delete()
        return scope
    except NoMatch:
        raise ScopeNotFound()
