from fastapi import APIRouter, Depends
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.ormar import paginate

from src.servers.schemas import ServerOut
from src.servers.services import servers_service

router = APIRouter()


@router.get("/")
async def get_servers(params: Params = Depends(), ip: str = None, port: int = None):
    """
    Get all servers
    :return:
    """
    if ip and port:
        return await servers_service.get_one(ip=ip, port=port)
    return await servers_service.get_all(params=params)


@router.get("/status")
async def get_servers_status():
    """
    Get all servers' status
    :return:
    """
    servers_status = await servers_service.get_status()
    return servers_status


@router.get("/{server_id}", response_model=ServerOut)
async def get_server(server_id: int):
    """
    Get server by id
    :param server_id:
    :return:
    """
    return await servers_service.get_one(id=server_id)
