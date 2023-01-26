from fastapi import APIRouter, Depends, Security
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Page, Params
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.ormar import paginate
from ormar import NoMatch

from src.auth.dependencies import get_admin_user
from src.scopes.enums import ScopesAdminEventsEnum
from src.scopes.exceptions import ScopeNotFound
from src.scopes.models import Scope
from src.scopes.schemas import ScopeOut, CreateScopeSchema
from src.scopes.utils import _get_scopes, _get_scope, _create_scope, _delete_scope
from src.users.models import User

router = APIRouter()


@router.get("", response_model=Page[ScopeOut])
async def admin_get_scopes(params: Params = Depends(),
                           user: User = Security(get_admin_user, scopes=["scopes:all"])) -> AbstractPage[ScopeOut]:
    """
    Admin get scopes.
    :param params:
    :param user:
    :return:
    """
    dispatch(ScopesAdminEventsEnum.GET_ALL_PRE, payload={"data": params, "user": user})
    scopes = await _get_scopes(params)
    dispatch(ScopesAdminEventsEnum.GET_ALL_POST, payload={"data": scopes, "user": user})
    return scopes


@router.get("/{scope_id}", response_model=ScopeOut)
async def admin_get_scope(scope_id: int, user: User = Security(get_admin_user, scopes=["scopes:retrieve"])):
    dispatch(ScopesAdminEventsEnum.GET_ONE_PRE, payload={"data": scope_id, "user": user})
    scope = await _get_scope(scope_id)
    dispatch(ScopesAdminEventsEnum.GET_ONE_POST, payload={"data": scope, "user": user})
    return scope


@router.post("", response_model=ScopeOut)
async def admin_create_scope(scope_data: CreateScopeSchema,
                             user: User = Security(get_admin_user, scopes=["scopes:create"])) -> ScopeOut:
    """
    Admin create scope.
    :param scope_data:
    :param user:
    :return:
    """
    dispatch(ScopesAdminEventsEnum.CREATE_PRE, payload={"data": scope_data, "user": user})
    scope = await _create_scope(scope_data)
    dispatch(ScopesAdminEventsEnum.CREATE_POST, payload={"data": scope, "user": user})
    return scope


@router.delete("/{scope_id}", response_model=ScopeOut)
async def admin_delete_scope(scope_id: int,
                             user: User = Security(get_admin_user, scopes=["scopes:delete"])) -> ScopeOut:
    """
    Admin delete scope.
    :param scope_id:
    :param user:
    :return:
    """
    dispatch(ScopesAdminEventsEnum.DELETE_PRE, payload={"data": scope_id, "user": user})
    scope = await _delete_scope(scope_id)
    dispatch(ScopesAdminEventsEnum.DELETE_POST, payload={"data": scope, "user": user})
    return scope
