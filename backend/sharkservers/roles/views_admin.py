"""Views for admin roles."""
from fastapi import APIRouter, Depends, Security
from fastapi_pagination import Page, Params

from sharkservers.auth.dependencies import get_admin_user
from sharkservers.roles.dependencies import get_roles_service, get_valid_role
from sharkservers.roles.models import Role
from sharkservers.roles.schemas import (
    CreateRoleSchema,
    RoleOut,
    RoleOutWithScopes,
    UpdateRoleSchema,
)
from sharkservers.roles.services import RoleService
from sharkservers.scopes.dependencies import get_scopes_service
from sharkservers.scopes.services import ScopeService

router = APIRouter()


@router.get("", dependencies=[Security(get_admin_user, scopes=["roles:all"])])
async def admin_get_roles(
    params: Params = Depends(),
    roles_service: RoleService = Depends(get_roles_service),
) -> Page[RoleOut]:
    """
    Retrieve all roles with pagination.

    Args:
    ----
        params (Params, optional): The query parameters for pagination. Defaults to Depends().
        admin_user (User, optional): The authenticated admin user. Defaults to Security(get_admin_user, scopes=["roles:all"]).
        roles_service (RoleService, optional): The service for managing roles. Defaults to Depends(get_roles_service).

    Returns:
    -------
        Page[RoleOut]: The paginated list of roles.
    """
    return await roles_service.get_all(params=params)


@router.get(
    "/{role_id}",
    dependencies=[Security(get_admin_user, scopes=["roles:retrieve"])],
)
async def admin_get_role(
    role: Role = Depends(get_valid_role),
) -> RoleOutWithScopes:
    """
    Retrieve the details of a role.

    Args:
    ----
        role (Role): The role object to retrieve details for.

    Returns:
    -------
        RoleOutWithScopes: The role object with associated scopes.

    """
    return role


@router.post("", dependencies=[Security(get_admin_user, scopes=["roles:create"])])
async def admin_create_role(
    role_data: CreateRoleSchema,
    roles_service: RoleService = Depends(get_roles_service),
    scopes_service: ScopeService = Depends(get_scopes_service),
) -> RoleOutWithScopes:
    """
    Admin endpoint to create a new role.

    Args:
    ----
        role_data (CreateRoleSchema): The data for creating the role.
        roles_service (RoleService, optional): The service for managing roles. Defaults to Depends(get_roles_service).
        scopes_service (ScopeService, optional): The service for managing scopes. Defaults to Depends(get_scopes_service).

    Returns:
    -------
        The newly created role.
    """
    return await roles_service.admin_create_role(role_data, scopes_service)


@router.delete(
    "/{role_id}",
    dependencies=[Security(get_admin_user, scopes=["roles:delete"])],
)
async def admin_delete_role(
    role: Role = Depends(get_valid_role),
    roles_service: RoleService = Depends(get_roles_service),
) -> RoleOutWithScopes:
    """
    Delete a role.

    Args:
    ----
        role (Role): The role to be deleted.
        roles_service (RoleService): The service used to delete the role.

    Returns:
    -------
        RoleOutWithScopes: The deleted role.

    """
    await roles_service.delete(_id=role.id)
    return role


@router.put(
    "/{role_id}",
    dependencies=[Security(get_admin_user, scopes=["roles:update"])],
)
async def admin_update_role(
    update_role_data: UpdateRoleSchema,
    role: Role = Depends(get_valid_role),
    scopes_service: ScopeService = Depends(get_scopes_service),
) -> RoleOutWithScopes:
    """
    Update a role with the provided data.

    Args:
    ----
        update_role_data (UpdateRoleSchema): The data to update the role with.
        role (Role): The role to be updated.
        scopes_service (ScopeService): The service to handle scopes.

    Returns:
    -------
        Role: The updated role.
    """
    update_role_data_dict = update_role_data.dict(exclude_unset=True)
    scopes_ids = update_role_data_dict.pop("scopes", None)
    scopes_list = []
    if scopes_ids:
        # Get scopes by ids
        for scope_id in scopes_ids:
            scope = await scopes_service.get_one(id=scope_id)
            scopes_list.append(scope)

        # First remove all scopes from role
        for _scope in role.scopes:
            await role.scopes.remove(_scope)
        # Then add new scopes to role
        for scope in scopes_list:
            await role.scopes.add(scope)
    await role.update(**update_role_data_dict)
    return role
