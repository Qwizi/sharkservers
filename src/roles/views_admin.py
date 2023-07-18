from fastapi import APIRouter, Security, Depends
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Page, Params
from fastapi_pagination.bases import AbstractPage
from ormar import NoMatch

from src.auth.dependencies import get_admin_user
from src.roles.dependencies import get_roles_service, get_valid_role
from src.roles.enums import RolesAdminEventsEnum
from src.roles.exceptions import role_not_found_exception
from src.roles.models import Role
from src.roles.schemas import RoleOut, RoleOutWithScopes, CreateRoleSchema
from src.roles.services import RoleService
from src.roles.utils import _delete_role
from src.scopes.dependencies import get_scopes_service
from src.scopes.models import Scope
from src.scopes.services import ScopeService
from src.users.models import User

router = APIRouter()


@router.get("", response_model=Page[RoleOut])
async def admin_get_roles(
        params: Params = Depends(),
        admin_user: User = Security(get_admin_user, scopes=["roles:all"]),
        roles_service: RoleService = Depends(get_roles_service),
) -> AbstractPage[RoleOut]:
    """
    Admin get all roles.
    :param roles_service:
    :param params:
    :param admin_user:
    :return AbstractPag[RoleOut]:
    """
    dispatch(RolesAdminEventsEnum.GET_ALL_PRE, payload={"data": params})
    roles = await roles_service.get_all(params=params)
    dispatch(RolesAdminEventsEnum.GET_ALL_POST, payload={"data": roles})
    return roles


@router.get("/{role_id}", response_model=RoleOutWithScopes)
async def admin_get_role(
        role: Role = Depends(get_valid_role), user: User = Security(get_admin_user, scopes=["roles:retrieve"])
) -> RoleOutWithScopes:
    """
    Admin get role by id.
    :param role:
    :param role_id:
    :param user:
    :return:
    """
    dispatch(RolesAdminEventsEnum.GET_ONE_PRE, payload={"data": role.id})
    dispatch(RolesAdminEventsEnum.GET_ONE_POST, payload={"data": role})
    return role


@router.post("", response_model=RoleOutWithScopes)
async def admin_create_role(
        role_data: CreateRoleSchema,
        admin_user: User = Security(get_admin_user, scopes=["roles:create"]),
        roles_service: RoleService = Depends(get_roles_service),
        scopes_service: ScopeService = Depends(get_scopes_service),
):
    """
    Admin create role.
    :param role_data:
    :param admin_user:
    :param roles_service:
    :param scopes_service:
    :return:
    """
    dispatch(RolesAdminEventsEnum.CREATE_PRE, payload={"data": role_data})
    new_role = await roles_service.admin_create_role(role_data, scopes_service)
    dispatch(RolesAdminEventsEnum.CREATE_POST, payload={"data": new_role})
    return new_role


@router.delete("/{role_id}")
async def admin_delete_role(
        role: Role = Depends(get_valid_role), user: User = Security(get_admin_user, scopes=["roles:delete"]),
        roles_service: RoleService = Depends(get_roles_service),
):
    """
    Admin delete role.
    :param role:
    :param user:
    :return:
    """
    dispatch(RolesAdminEventsEnum.DELETE_PRE, payload={"data": role.id})
    await roles_service.delete(_id=role.id)
    dispatch(RolesAdminEventsEnum.DELETE_POST, payload={"data": role})
    return role


@router.post("/{role_id}/scopes/add", response_model=RoleOut)
async def admin_add_scopes_to_role(
        role_id: int,
        scopes: list[int],
        user: User = Security(get_admin_user, scopes=["roles:create"]),
):
    role = await Role.objects.select_related(["scopes"]).get(id=role_id)
    if not role:
        raise role_not_found_exception
    for scope in scopes:
        try:
            scope = await Scope.objects.get(id=scope)
            await role.scopes.add(scope)
        except NoMatch:
            continue
    await role.load()
    return role
