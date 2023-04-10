from fastapi import Depends
from ormar import Model

from src.players.dependencies import get_valid_player_by_steamid
from src.players.models import Player
from src.servers.models import Server
from src.servers.services import (
    ServerService,
    ServerPlayerStatsService,
    ChatColorModuleService,
)


async def get_servers_service() -> ServerService:
    return ServerService()


async def get_server_player_stats_service() -> ServerPlayerStatsService:
    return ServerPlayerStatsService()


async def get_valid_server(
    server_id: int, servers_service: ServerService = Depends(get_servers_service)
) -> Model:
    return await servers_service.get_one(id=server_id)


async def get_valid_server_player_stats(
    server: Server = Depends(get_valid_server),
    player: Player = Depends(get_valid_player_by_steamid),
    server_player_stats_service: ServerPlayerStatsService = Depends(
        get_server_player_stats_service
    ),
):
    return await server_player_stats_service.get_one(
        server=server, player=player, related=["player", "server", "stats"]
    )


async def get_chat_color_module_service() -> ChatColorModuleService:
    return ChatColorModuleService()
