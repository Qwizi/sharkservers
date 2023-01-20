from asyncpg import UniqueViolationError
from fastapi import APIRouter, Security, Depends, HTTPException
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Page, Params
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.ormar import paginate
from ormar import NoMatch
from psycopg2 import IntegrityError
from sqlite3 import IntegrityError as SQLIntegrityError

from src.auth.dependencies import get_admin_user
from src.roles.enums import RolesAdminEventsEnum
from src.roles.exceptions import role_exists_exception, role_not_found_exception
from src.roles.models import Role
from src.roles.schemas import RoleOut, RoleOutWithScopes, CreateRoleSchema
from src.roles.utils import _get_roles, _get_role, _delete_role
from src.scopes.models import Scope
from src.users.models import User

router = APIRouter()


@router.get("", response_model=Page[RoleOut])
async def admin_get_roles(params: Params = Depends(),
                          user: User = Security(get_admin_user, scopes=["roles:get_all"])) -> AbstractPage[RoleOut]:
    """
    Admin get all roles.
    :param params:
    :param user:
    :return AbstractPag[RoleOut]:
    """
    dispatch(RolesAdminEventsEnum.GET_ALL_PRE, payload={"data": params})
    roles = await _get_roles(params)
    dispatch(RolesAdminEventsEnum.GET_ALL_POST, payload={"data": roles})
    return roles


@router.get("/{role_id}", response_model=RoleOutWithScopes)
async def admin_get_role(role_id: int,
                         user: User = Security(get_admin_user, scopes=["roles:retrieve"])) -> RoleOutWithScopes:
    """
    Admin get role by id.
    :param role_id:
    :param user:
    :return:
    """
    dispatch(RolesAdminEventsEnum.GET_ONE_PRE, payload={"data": role_id})
    roles = await _get_role(role_id)
    dispatch(RolesAdminEventsEnum.GET_ONE_POST, payload={"data": roles})
    return roles


@router.post("", response_model=RoleOutWithScopes)
async def admin_create_role(role_data: CreateRoleSchema,
                            user: User = Security(get_admin_user, scopes=["roles:create"])):
    scopes = None
    if role_data.scopes:
        scopes = await Scope.objects.filter(id__in=role_data.scopes).all()
        print(scopes)
    try:
        role = await Role.objects.create(
            name=role_data.name,
            color=role_data.color,
            is_staff=role_data.is_staff
        )
        if scopes:
            for scope in scopes:
                await role.scopes.add(scope)
        return role
    except UniqueViolationError as e:
        raise role_exists_exception


@router.delete("/{role_id}")
async def admin_delete_role(role_id: int, user: User = Security(get_admin_user, scopes=["roles:delete"])):
    dispatch(RolesAdminEventsEnum.DELETE_PRE, payload={"data": role_id})
    role = await _delete_role(role_id)
    dispatch(RolesAdminEventsEnum.DELETE_POST, payload={"data": role})
    return role


@router.post("/{role_id}/scopes/add", response_model=RoleOut)
async def admin_add_scopes_to_role(role_id: int, scopes: list[int],
                                   user: User = Security(get_admin_user, scopes=["roles:create"])):
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
