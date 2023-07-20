from fastapi import APIRouter, Depends, Security
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Page, Params
from fastapi_pagination.bases import AbstractPage

from src.auth.dependencies import get_admin_user
from src.scopes.dependencies import get_scopes_service, get_valid_scope
from src.scopes.enums import ScopesAdminEventsEnum
from src.scopes.models import Scope
from src.scopes.schemas import ScopeOut, CreateScopeSchema
from src.scopes.services import ScopeService
from src.scopes.utils import _get_scopes, _get_scope, _create_scope, _delete_scope
from src.users.models import User

router = APIRouter()


@router.get("", response_model=Page[ScopeOut])
async def admin_get_scopes(
        params: Params = Depends(),
        admin_user: User = Security(get_admin_user, scopes=["scopes:all"]),
        scopes_service: ScopeService = Depends(get_scopes_service),
) -> list[ScopeOut]:
    """
    Admin get scopes.
    :param scopes_service:
    :param params:
    :param     admin_user:
    :return:
    """
    dispatch(ScopesAdminEventsEnum.GET_ALL_PRE, payload={"data": params, "user": admin_user})
    scopes = await scopes_service.get_all(params=params)
    dispatch(ScopesAdminEventsEnum.GET_ALL_POST, payload={"data": scopes, "user": admin_user})
    return scopes


@router.get("/{scope_id}", response_model=ScopeOut)
async def admin_get_scope(
        scope: Scope = Depends(get_valid_scope),
        admin_user: User = Security(get_admin_user, scopes=["scopes:retrieve"]),
) -> ScopeOut:
    dispatch(
        ScopesAdminEventsEnum.GET_ONE_PRE, payload={"data": scope.id, "user": admin_user}
    )
    dispatch(ScopesAdminEventsEnum.GET_ONE_POST, payload={"data": scope, "user": admin_user})
    return scope


@router.post("", response_model=ScopeOut)
async def admin_create_scope(
        scope_data: CreateScopeSchema,
        admin_user: User = Security(get_admin_user, scopes=["scopes:create"]),
) -> ScopeOut:
    """
    Admin create scope.
    :param scope_data:
    :param admin_user:
    :return:
    """
    dispatch(
        ScopesAdminEventsEnum.CREATE_PRE, payload={"data": scope_data, "user": admin_user}
    )
    scope = await _create_scope(scope_data)
    dispatch(ScopesAdminEventsEnum.CREATE_POST, payload={"data": scope, "user": admin_user})
    return scope


@router.delete("/{scope_id}", response_model=ScopeOut)
async def admin_delete_scope(
        scope_id: int, user: User = Security(get_admin_user, scopes=["scopes:delete"])
) -> ScopeOut:
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
