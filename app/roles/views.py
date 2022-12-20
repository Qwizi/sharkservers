from fastapi import APIRouter, Depends
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Page, Params
from fastapi_pagination.bases import AbstractPage

from app.roles.enums import RolesEventsEnum
from app.roles.schemas import RoleOut, RoleOutWithScopes, RoleOutWithoutScopesAndUserRoles, StaffRolesSchema
from app.roles.utils import _get_roles, _get_staff_roles, _get_role

router = APIRouter()


@router.get("", response_model=Page[RoleOut], response_model_exclude_none=True)
async def get_roles(params: Params = Depends()) -> AbstractPage:
    """
    Get roles
    :param params:
    :return AbstractPage:
    """
    dispatch(event_name=RolesEventsEnum.GET_ALL_PRE, payload={"data": params})
    roles = await _get_roles(params)
    dispatch(event_name=RolesEventsEnum.GET_ALL_POST, payload={"data": roles})
    return roles


@router.get("/staff")
async def get_staff_roles():
    """
    Get staff roles
    :return:
    """
    """
    dispatch(event_name=RolesEventsEnum.STAFF_GET_ALL_PRE, payload={})
    roles = await _get_staff_roles()
    dispatch(event_name=RolesEventsEnum.STAFF_GET_ALL_POST, payload={"data": roles})
    return roles
    """
    return {"msg": "Not implemented"}


@router.get("/{role_id}", response_model=RoleOutWithScopes)
async def get_role(role_id: int) -> RoleOutWithScopes:
    """
    Get role by id
    :param role_id:
    :return:
    """
    dispatch(event_name=RolesEventsEnum.GET_ONE_PRE, payload={"data": role_id})
    role = await _get_role(role_id)
    dispatch(event_name=RolesEventsEnum.GET_ONE_POST, payload={"data": role})
    return role
