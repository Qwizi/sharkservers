from fastapi import APIRouter, Depends
from fastapi_pagination import Params
from sourcemod_api_client import CreateGroupSchema, Page_GroupOut_, GroupOut

from src.servers.dependencies import get_valid_server
from src.servers.models import Server

router = APIRouter()


@router.get("/{server_id}/admins/groups")
async def admin_get_server_admins_groups(
        params: Params = Depends(),
        server: Server = Depends(get_valid_server),
) -> Page_GroupOut_:
    """
    Get server admins groups
    :param servers_service:
    :param server:
    :return:
    """
    return await server.get_admins_groups(params=params)


@router.post("/{server_id}/admins/groups")
async def admin_create_server_admins_groups(
        data: CreateGroupSchema,
        server: Server = Depends(get_valid_server),
) -> GroupOut:
    """
    Create server admins groups
    :param servers_service:
    :param server:
    :return:
    """
    return await server.create_admin_group(data=data)


@router.get("/{server_id}/admins/groups/{group_id}")
async def admin_get_server_admins_group(
        group_id: int,
        server: Server = Depends(get_valid_server),
) -> Page_GroupOut_:
    """
    Get server admins group
    :param servers_service:
    :param server:
    :return:
    """
    return await server.get_admins_group(group_id=group_id)


@router.delete("/{server_id}/admins/groups/{group_id}")
async def admin_delete_server_admins_group(
        group_id: int,
        server: Server = Depends(get_valid_server),
) -> Page_GroupOut_:
    """
    Delete server admins group
    :param servers_service:
    :param server:
    :return:
    """
    return await server.delete_admin_group(group_id=group_id)
