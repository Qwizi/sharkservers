from fastapi import Depends
from ormar import Model

from src.servers.services import (
    ServerService,
    ChatColorModuleService
)


async def get_servers_service() -> ServerService:
    return ServerService()


async def get_valid_server(
        server_id: int, servers_service: ServerService = Depends(get_servers_service)
) -> Model:
    return await servers_service.get_one(id=server_id, related=["admin_role"])


async def get_chat_color_module_service() -> ChatColorModuleService:
    return ChatColorModuleService()
