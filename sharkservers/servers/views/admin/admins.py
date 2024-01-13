from fastapi import APIRouter, Depends
from fastapi_pagination import Params
from sourcemod_api_client import (
    AdminOut,
    CreateAdminSchema,
    Page_AdminOut_,
    UpdateAdminSchema,
)

from sharkservers.servers.dependencies import get_valid_server
from sharkservers.servers.models import Server

router = APIRouter()


@router.get("/{server_id}/admins")
async def admin_get_server_admins(
    params: Params = Depends(),
    server: Server = Depends(get_valid_server),
) -> Page_AdminOut_:
    """
    Get server admins
    :param servers_service:
    :param server:
    :return:
    """
    return await server.get_admins(params=params)


@router.post("/{server_id}/admins")
async def admin_create_server_admin(
    data: CreateAdminSchema,
    server: Server = Depends(get_valid_server),
) -> AdminOut:
    """
    Create server admin
    :param servers_service:
    :param server:
    :return:
    """
    return await server.create_admin(data=data)


@router.get("/{server_id}/admins/{identity}")
async def admin_get_server_admin(
    identity: str,
    server: Server = Depends(get_valid_server),
) -> AdminOut:
    """
    Get server admin
    :param servers_service:
    :param server:
    :return:
    """
    return await server.get_admin(identity=identity)


@router.put("/{server_id}/admins/{identity}")
async def admin_update_server_admin(
    identity: str,
    data: UpdateAdminSchema,
    server: Server = Depends(get_valid_server),
) -> AdminOut:
    """
    Update server admin
    :param servers_service:
    :param server:
    :return:
    """
    return await server.update_admin(identity=identity, data=data)


@router.delete("/{server_id}/admins/{identity}")
async def admin_delete_server_admin(
    identity: str,
    server: Server = Depends(get_valid_server),
) -> AdminOut:
    """
    Delete server admin
    :param servers_service:
    :param server:
    :return:
    """
    return await server.delete_admin(identity=identity)
