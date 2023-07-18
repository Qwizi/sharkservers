from fastapi import APIRouter, Depends
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Page, Params

from src.roles.dependencies import get_valid_role, get_roles_service
from src.roles.enums import RolesEventsEnum
from src.roles.models import Role
from src.roles.schemas import (
    RoleOut,
    RoleOutWithScopes,
)
from src.roles.services import RoleService

router = APIRouter()


@router.get("", response_model_exclude_none=True)
async def get_roles(
        params: Params = Depends(), roles_service: RoleService = Depends(get_roles_service)
) -> Page[RoleOut]:
    """
    Get roles
    :param roles_service:
    :param params:
    :return AbstractPage:
    """
    dispatch(event_name=RolesEventsEnum.GET_ALL_PRE, payload={"data": params})
    roles = await roles_service.get_all(params=params)
    dispatch(event_name=RolesEventsEnum.GET_ALL_POST, payload={"data": roles})
    return roles


@router.get("/{role_id}", response_model=RoleOutWithScopes)
async def get_role(role: Role = Depends(get_valid_role)) -> RoleOutWithScopes:
    """
    Get role by id
    :param role:
    :return:
    """
    dispatch(event_name=RolesEventsEnum.GET_ONE_PRE, payload={"data": role.id})
    dispatch(event_name=RolesEventsEnum.GET_ONE_POST, payload={"data": role})
    return role
