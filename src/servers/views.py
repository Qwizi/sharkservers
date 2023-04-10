import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.ormar import paginate
from ormar import Model

from src.logger import logger
from src.players.dependencies import (
    get_valid_player_by_steamid,
    get_player_stats_service,
)
from src.players.models import Player
from src.players.schemas import UpdatePlayerStatsSchema
from src.players.services import PlayerStatsService
from src.servers.dependencies import (
    get_servers_service,
    get_valid_server,
    get_server_player_stats_service,
    get_valid_server_player_stats,
)
from src.servers.models import Server
from src.servers.schemas import ServerOut
from src.servers.services import ServerService, ServerPlayerStatsService

router = APIRouter()


@router.get("/")
async def get_servers(
    params: Params = Depends(),
    ip: str = None,
    port: int = None,
    servers_service: ServerService = Depends(get_servers_service),
):
    """
    Get all servers
    :return:
    """
    if ip and port:
        return await servers_service.get_one(ip=ip, port=port)
    return await servers_service.get_all(params=params)


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


@router.get("/{server_id}", response_model=ServerOut)
async def get_server(server: Model = Depends(get_valid_server)):
    """
    Get server by id
    :param server:
    :param server_id:
    :return:
    """
    return server


@router.get("/{server_id}/players/{steamid64}/stats")
async def get_server_player_stats(
    server_player_stats_service: ServerPlayerStatsService = Depends(
        get_server_player_stats_service
    ),
    server_player_stats: Model = Depends(get_valid_server_player_stats),
):
    """
    Get server player stats
    :param server_player_stats:
    :param player:
    :param server_player_stats_service:
    :param server:
    :return:
    """
    stats = await server_player_stats.stats.sum(
        [
            "kills",
            "points",
            "deaths",
            "assists",
            "damage",
            "damage_taken",
            "healing",
            "healing_taken",
            "headshots",
            "backstabs",
            "dominations",
            "revenges",
            "captures",
            "defends",
            "ubers",
            "teleports",
            "suicides",
            "sentries",
            "buildings_destroyed",
            "time_played",
        ]
    )
    logger.info(stats)
    return {
        "server": server_player_stats.server,
        "player": server_player_stats.player,
        "stats": stats,
    }


@router.post("/{server_id}/players/{steamid64}/stats")
async def create_server_player_stats(
    server: Server = Depends(get_valid_server),
    player: Player = Depends(get_valid_player_by_steamid),
    server_player_stats_service: ServerPlayerStatsService = Depends(
        get_server_player_stats_service
    ),
):
    """
    Create server player stats
    :param player:
    :param server_player_stats_service:
    :param server:
    :return:
    """
    if await server_player_stats_service.Meta.model.objects.filter(
        server=server, player=player
    ).exists():
        return HTTPException(status_code=400, detail="Stats already exists")
    return await server_player_stats_service.create(server=server, player=player)


@router.put("/{server_id}/players/{steamid64}/stats")
async def update_server_player_stats(
    player_stats_data: UpdatePlayerStatsSchema,
    server_player_stats: Model = Depends(get_valid_server_player_stats),
    player_stats_service: PlayerStatsService = Depends(get_player_stats_service),
):
    """
    Update server player stats
    :param player_stats_service:
    :param server_player_stats:
    :return:
    """
    today = datetime.date.today()
    player_stats, created = await player_stats_service.Meta.model.objects.get_or_create(
        date=today
    )
    if created:
        await server_player_stats.stats.add(player_stats)

    player_stats_data_dict = player_stats_data.dict()
    player_stats_dict = player_stats.dict()
    for key, value in player_stats_data_dict.items():
        old_value = player_stats_dict[key]
        if value is None:
            continue
        logger.info(f"{key}: {old_value} + {value}")
        await player_stats.update(**{key: old_value + value})
    return player_stats
