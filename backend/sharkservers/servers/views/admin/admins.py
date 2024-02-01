"""Admin views for servers."""
from fastapi import APIRouter, Depends, Security
from fastapi_pagination import Params
from sourcemod_api_client import (
    AdminOut,
    CreateAdminSchema,
    Page_AdminOut_,
    UpdateAdminSchema,
)

from sharkservers.auth.dependencies import get_admin_user
from sharkservers.servers.dependencies import get_valid_server
from sharkservers.servers.models import Server

router = APIRouter(dependencies=[Security(get_admin_user)])


@router.get("/{server_id}/admins")
async def admin_get_server_admins(
    params: Params = Depends(),
    server: Server = Depends(get_valid_server),
) -> Page_AdminOut_:
    """
    Retrieve the list of admins for a server.

    Args:
    ----
        params (Params): The query parameters for filtering and pagination.
        server (Server): The server for which to retrieve the admins.

    Returns:
    -------
        Page_AdminOut_: The paginated list of admins for the server.
    """
    return await server.get_admins(params=params)


@router.post("/{server_id}/admins")
async def admin_create_server_admin(
    data: CreateAdminSchema,
    server: Server = Depends(get_valid_server),
) -> AdminOut:
    """
    Create a server admin.

    Args:
    ----
        data (CreateAdminSchema): The data for creating the admin.
        server (Server): The server instance.

    Returns:
    -------
        AdminOut: The created admin.
    """
    return await server.create_admin(data=data)


@router.get("/{server_id}/admins/{identity}")
async def admin_get_server_admin(
    identity: str,
    server: Server = Depends(get_valid_server),
) -> AdminOut:
    """
    Retrieve the admin information for a specific server.

    Args:
    ----
        identity (str): The identity of the admin.
        server (Server): The server object.

    Returns:
    -------
        AdminOut: The admin information.

    """
    return await server.get_admin(identity=identity)


@router.put("/{server_id}/admins/{identity}")
async def admin_update_server_admin(
    identity: str,
    data: UpdateAdminSchema,
    server: Server = Depends(get_valid_server),
) -> AdminOut:
    """
    Update the server admin with the given identity using the provided data.

    Args:
    ----
        identity (str): The identity of the server admin to update.
        data (UpdateAdminSchema): The updated admin data.
        server (Server): The server instance.

    Returns:
    -------
        AdminOut: The updated server admin.

    """
    return await server.update_admin(identity=identity, data=data)


@router.delete("/{server_id}/admins/{identity}")
async def admin_delete_server_admin(
    identity: str,
    server: Server = Depends(get_valid_server),
) -> AdminOut:
    """
    Delete a server admin with the given identity from the server.

    Args:
    ----
        identity (str): The identity of the admin to be deleted.
        server (Server): The server from which the admin should be deleted.

    Returns:
    -------
        AdminOut: The deleted admin.

    """
    return await server.delete_admin(identity=identity)
