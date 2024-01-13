"""Views for roles."""  # noqa: EXE002
from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params

from sharkservers.roles.dependencies import get_roles_service, get_valid_role
from sharkservers.roles.models import Role
from sharkservers.roles.schemas import (
    RoleOut,
    RoleOutWithScopes,
)
from sharkservers.roles.services import RoleService

router = APIRouter()


@router.get("")
async def get_roles(
    params: Params = Depends(),  # noqa: B008
    roles_service: RoleService = Depends(get_roles_service),  # noqa: B008
) -> Page[RoleOut]:
    """
    Retrieve all roles based on the provided parameters.

    Args:
    ----
        params (Params): The parameters for filtering and pagination.
        roles_service (RoleService): The service for retrieving roles.

    Returns:
    -------
        Page[RoleOut]: A paginated list of RoleOut objects.
    """
    return await roles_service.get_all(params=params)


@router.get("/{role_id}")
async def get_role(role: Role = Depends(get_valid_role)) -> RoleOutWithScopes:  # noqa: B008
    """
    Retrieve a role by its ID.

    Args:
    ----
        role (Role): The role object.

    Returns:
    -------
        RoleOutWithScopes: The role object with associated scopes.

    """
    return role
