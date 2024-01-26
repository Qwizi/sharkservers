"""Admin server views."""
from fastapi import APIRouter, Depends

from sharkservers.auth.dependencies import get_admin_user
from sharkservers.servers.dependencies import get_servers_service, get_valid_server
from sharkservers.servers.models import Server
from sharkservers.servers.schemas import (
    CreateServerSchema,
    ServerOut,
    UpdateServerSchema,
)
from sharkservers.servers.services import ServerService

router = APIRouter(dependencies=[Depends(get_admin_user)])


@router.get("")
async def admin_get_servers(
    servers_service: ServerService = Depends(get_servers_service),
) -> ServerOut:
    """
    Retrieve all servers with their associated admin role.

    Args:
    ----
        servers_service (ServerService): The server service instance.

    Returns:
    -------
        ServerOut: The server data with the associated admin role.
    """
    return await servers_service.get_all(related=["admin_role"])


@router.post("")
async def admin_create_server(
    server_data: CreateServerSchema,
    servers_service: ServerService = Depends(get_servers_service),
) -> ServerOut:
    """
    Create a new server using the provided server data.

    Args:
    ----
        server_data (CreateServerSchema): The data for creating the server.
        servers_service (ServerService): The server service instance.

    Returns:
    -------
        ServerOut: The created server.

    """
    return await servers_service.create(**server_data.dict())


@router.get("/{server_id}")
async def admin_get_server(
    server: Server = Depends(get_valid_server),
) -> ServerOut:
    """
    Retrieve the details of a server for admin purposes.

    Args:
    ----
        server (Server): The server object to retrieve details for.

    Returns:
    -------
        ServerOut: The server details.

    """
    return server


@router.put("/{server_id}")
async def admin_update_server(
    server_data: UpdateServerSchema,
    server: Server = Depends(get_valid_server),
) -> ServerOut:
    """
    Update the server with the provided data.

    Args:
    ----
        server_data (UpdateServerSchema): The data to update the server with.
        server (Server): The server to be updated.

    Returns:
    -------
        ServerOut: The updated server.
    """
    return await server.update(**server_data.dict())


@router.delete("/{server_id}")
async def admin_delete_server(
    server: Server = Depends(get_valid_server),
    servers_service: ServerService = Depends(get_servers_service),
) -> bool:
    """
    Delete the specified server.

    Args:
    ----
        server (Server): The server to be deleted.
        servers_service (ServerService): The server service instance.

    Returns:
    -------
        bool: True if the server is successfully deleted, False otherwise.
    """
    return await servers_service.delete(server.id)
