from fastapi import APIRouter, Depends
from fastapi_pagination import Params, Page
from ormar import Model

from src.servers.dependencies import (
    get_servers_service,
    get_valid_server,
)
from src.servers.schemas import (
    ServerOut,
)
from src.servers.services import ServerService

router = APIRouter()


@router.get("/")
async def get_servers(
        params: Params = Depends(),
        ip: str = None,
        port: int = None,
        servers_service: ServerService = Depends(get_servers_service),
) -> Page[ServerOut]:
    """
    Get all servers
    :return:
    """
    if ip and port:
        return await servers_service.get_one(ip=ip, port=port)
    return await servers_service.get_all(params=params, related=["admin_role"])


@router.get("/status")
async def get_servers_status(
        servers_service: ServerService = Depends(get_servers_service),
):
    """
    Get all servers' status
    :return:
    """
    servers_status = await servers_service.get_status()
    return servers_status


@router.get("/{server_id}")
async def get_server(server: Model = Depends(get_valid_server)) -> ServerOut:
    """
    Get server by id
    :param server:
    :param server_id:
    :return:
    """
    return server
