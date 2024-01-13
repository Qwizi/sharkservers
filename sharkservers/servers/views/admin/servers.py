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
    Get all servers
    :return:
    """
    return await servers_service.get_all(related=["admin_role"])


@router.post("")
async def admin_create_server(
    server_data: CreateServerSchema,
    servers_service: ServerService = Depends(get_servers_service),
) -> ServerOut:
    """
    Create a new server
    :param servers_service:
    :param server_data:
    :return:
    """
    return await servers_service.create(**server_data.dict())


@router.get("/{server_id}")
async def admin_get_server(
    server: Server = Depends(get_valid_server),
    servers_service: ServerService = Depends(get_servers_service),
) -> ServerOut:
    """
    Get server by id
    :param servers_service:
    :param server:
    :return:
    """
    return server


@router.put("/{server_id}")
async def admin_update_server(
    server_data: UpdateServerSchema,
    server: Server = Depends(get_valid_server),
    servers_service: ServerService = Depends(get_servers_service),
) -> ServerOut:
    """
    Update a server
    :param servers_service:
    :param server:
    :param server_data:
    :return:
    """
    return await server.update(**server_data.dict())


@router.delete("/{server_id}")
async def admin_delete_server(
    server: Server = Depends(get_valid_server),
    servers_service: ServerService = Depends(get_servers_service),
):
    """
    Delete a server
    :param servers_service:
    :param server:
    :return:
    """
    return await servers_service.delete(server.id)
