from fastapi import APIRouter, Depends, Security
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Page, Params
from fastapi_pagination.bases import AbstractPage

from src.auth.dependencies import get_admin_user
from src.scopes.dependencies import get_scopes_service, get_valid_scope
from src.scopes.enums import ScopesAdminEventsEnum
from src.scopes.models import Scope
from src.scopes.schemas import ScopeOut, CreateScopeSchema, UpdateScopeSchema
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
        scopes_service: ScopeService = Depends(get_scopes_service),
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
    scope = await scopes_service.create(**scope_data.dict())
    dispatch(ScopesAdminEventsEnum.CREATE_POST, payload={"data": scope, "user": admin_user})
    return scope


@router.delete("/{scope_id}", response_model=ScopeOut)
async def admin_delete_scope(
        scope: Scope = Depends(get_valid_scope), admin_user: User = Security(get_admin_user, scopes=["scopes:delete"]),
        scopes_service: ScopeService = Depends(get_scopes_service),
) -> ScopeOut:
    """
    Admin delete scope.
    :param scope:
    :param admin_user:
    :return:
    """
    dispatch(ScopesAdminEventsEnum.DELETE_PRE, payload={"data": scope, "user": admin_user})
    scope = await scopes_service.delete(_id=scope.id)
    dispatch(ScopesAdminEventsEnum.DELETE_POST, payload={"data": scope, "user": admin_user})
    return scope


@router.put("/{scope_id}")
async def admin_update_scope(
        update_scope_data: UpdateScopeSchema,
        scope: Scope = Depends(get_valid_scope),
        admin_user: User = Security(get_admin_user, scopes=["scopes:update"]),
) -> ScopeOut:
    """
    Admin update scope.
    :param update_scope_data:
    :param scopes_service:
    :param scope:
    :param admin_user:
    :return:
    """
    dispatch(ScopesAdminEventsEnum.UPDATE_PRE, payload={"data": scope, "user": admin_user})
    await scope.update(**update_scope_data.dict(exclude_unset=True, exclude_none=True))
    dispatch(ScopesAdminEventsEnum.UPDATE_POST, payload={"data": scope, "user": admin_user})
    return scope
