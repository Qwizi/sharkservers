from fastapi import Depends
from ormar import Model

from src.servers.services import ServerService


async def get_servers_service() -> ServerService:
    return ServerService()


async def get_valid_server(
    server_id: int, servers_service: ServerService = Depends(get_servers_service)
) -> Model:
    return await servers_service.get_one(id=server_id)
