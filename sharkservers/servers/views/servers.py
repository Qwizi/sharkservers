"""Server views."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from ormar import Model

from sharkservers.servers.dependencies import (
    get_servers_service,
    get_valid_server,
)
from sharkservers.servers.schemas import (
    ServerOut,
    ServerStatusSchema,
)
from sharkservers.servers.services import ServerService

router = APIRouter()


@router.get("/")
async def get_servers(
    params: Params = Depends(),
    ip: str | None = None,
    port: int | None = None,
    servers_service: ServerService = Depends(get_servers_service),
) -> Page[ServerOut]:
    """
    Retrieve servers based on the provided parameters.

    Args:
    ----
        params (Params, optional): The query parameters for filtering and pagination. Defaults to Depends().
        ip (str, optional): The IP address of the server to retrieve. Defaults to None.
        port (int, optional): The port of the server to retrieve. Defaults to None.
        servers_service (ServerService, optional): The server service dependency. Defaults to Depends(get_servers_service).

    Returns:
    -------
        Page[ServerOut]: A paginated list of server objects.

    """
    if ip and port:
        return await servers_service.get_one(ip=ip, port=port)
    return await servers_service.get_all(params=params, related=["admin_role"])


@router.get("/status")
async def get_servers_status(
    servers_service: ServerService = Depends(get_servers_service),
) -> list[ServerStatusSchema]:
    """
    Retrieve the status of servers.

    Args:
    ----
        servers_service (ServerService): The server service instance used to retrieve server status.

    Returns:
    -------
        list[ServerStatusSchema]: A list of server status objects.

    Raises:
    ------
        ConnectionRefusedError: If there is an error retrieving the server status.
    """
    return await servers_service.get_status()


@router.get("/{server_id}")
async def get_server(server: Model = Depends(get_valid_server)) -> ServerOut:
    """
    Retrieve a server based on the provided server model.

    Args:
    ----
        server (Model): The server model to retrieve.

    Returns:
    -------
        ServerOut: The retrieved server.

    """
    return server
