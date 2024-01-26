"""Admins groups views."""
from fastapi import APIRouter, Depends
from fastapi_pagination import Params
from sourcemod_api_client import CreateGroupSchema, GroupOut, Page_GroupOut_

from sharkservers.servers.dependencies import get_valid_server
from sharkservers.servers.models import Server

router = APIRouter()


@router.get("/{server_id}/admins/groups")
async def admin_get_server_admins_groups(
    params: Params = Depends(),
    server: Server = Depends(get_valid_server),
) -> Page_GroupOut_:
    """
    Retrieve the admins groups for a server.

    Args:
    ----
        params (Params): The parameters for the request.
        server (Server): The server to retrieve the admins groups for.

    Returns:
    -------
        Page_GroupOut_: The paginated list of admins groups.
    """
    return await server.get_admins_groups(params=params)


@router.post("/{server_id}/admins/groups")
async def admin_create_server_admins_groups(
    data: CreateGroupSchema,
    server: Server = Depends(get_valid_server),
) -> GroupOut:
    """
    Create a new admin group for a server.

    Args:
    ----
        data (CreateGroupSchema): The data for creating the group.
        server (Server): The server for which the group is being created.

    Returns:
    -------
        GroupOut: The created admin group.
    """
    return await server.create_admin_group(data=data)


@router.get("/{server_id}/admins/groups/{group_id}")
async def admin_get_server_admins_group(
    group_id: int,
    server: Server = Depends(get_valid_server),
) -> GroupOut:
    """
    Retrieve the admins group of a server by its group ID.

    Args:
    ----
        group_id (int): The ID of the admins group.
        server (Server): The server object.

    Returns:
    -------
        GroupOut: The admins group information.

    """
    return await server.get_admins_group(group_id=group_id)


@router.delete("/{server_id}/admins/groups/{group_id}")
async def admin_delete_server_admins_group(
    group_id: int,
    server: Server = Depends(get_valid_server),
) -> GroupOut:
    """
    Delete an admin group from the server.

    Args:
    ----
        group_id (int): The ID of the admin group to delete.
        server (Server): The server object.

    Returns:
    -------
        GroupOut: The deleted admin group.
    """
    return await server.delete_admin_group(group_id=group_id)
