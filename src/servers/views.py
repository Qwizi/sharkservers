
from fastapi import APIRouter, Depends
from fastapi_pagination import Params, Page
from ormar import Model
from src.players.dependencies import (
    get_valid_player_by_steamid,
    get_players_service,
)
from src.players.services import  PlayerService
from src.servers.dependencies import (
    get_servers_service,
    get_valid_server,
    get_chat_color_module_service,
)
from src.servers.models import Server
from src.servers.schemas import (
    ServerOut,
    CreatePlayerChatColorSchema,
    UpdatePlayerChatColorSchema,
)
from src.servers.services import (
    ServerService,
    ChatColorModuleService,
)

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


@router.get("/{server_id}")
async def get_server(server: Model = Depends(get_valid_server)) -> ServerOut:
    """
    Get server by id
    :param server:
    :param server_id:
    :return:
    """
    return server


"""

@router.get("/{server_id}/player-stats")
async def get_players_stats(
    params: Params = Depends(),
    server: Server = Depends(get_valid_server),
    server_player_stats_service: ServerPlayerStatsService = Depends(
        get_server_player_stats_service
    ),
):

    players_stats_from_db = await server_player_stats_service.get_all(
        params=params,
        server=server,
        related=["player", "server", "stats"],
        order_by=["-points"],
    )
    players_stats_from_db_copy = players_stats_from_db.copy()
    server_players_stats_dict = players_stats_from_db_copy.dict()

    for index, server_player_stats in enumerate(players_stats_from_db_copy.items):
        logger.info(index)
        stats = await server_player_stats.stats.sum(
            [
                "kills",
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

        server_players_stats_dict["items"][index]["total_stats"] = stats
    return server_players_stats_dict


@router.get("/{server_id}/player-stats/{steamid64}")
async def get_server_player_stats(
    server_player_stats_service: ServerPlayerStatsService = Depends(
        get_server_player_stats_service
    ),
    server_player_stats: Model = Depends(get_valid_server_player_stats),
):
    stats = await server_player_stats.stats.sum(
        [
            "kills",
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
        "points": server_player_stats.points,
    }


@router.post("/{server_id}/player-stats/{steamid64}")
async def create_server_player_stats(
    server: Server = Depends(get_valid_server),
    player: Player = Depends(get_valid_player_by_steamid),
    server_player_stats_service: ServerPlayerStatsService = Depends(
        get_server_player_stats_service
    ),
):
    if await server_player_stats_service.Meta.model.objects.filter(
        server=server, player=player
    ).exists():
        return HTTPException(status_code=400, detail="Stats already exists")
    return await server_player_stats_service.create(server=server, player=player)


@router.put("/{server_id}/player-stats/{steamid64}")
async def update_server_player_stats(
    player_stats_data: UpdatePlayerStatsSchema,
    server_player_stats: Model = Depends(get_valid_server_player_stats),
    player_stats_service: PlayerStatsService = Depends(get_player_stats_service),
):
    today = datetime.date.today()
    player_stats, created = await server_player_stats.stats.get_or_create(date=today)
    if created:
        await server_player_stats.stats.add(player_stats)

    player_stats_data_dict = player_stats_data.dict()
    player_stats_dict = player_stats.dict()
    for key, value in player_stats_data_dict.items():
        old_value = player_stats_dict[key]
        if value is None:
            continue
        if key == "kills":
            points = 5
            points_multiple = points * value
            points_to_add = server_player_stats.points + points_multiple
            await server_player_stats.update(points=points_to_add)
        elif key == "assists":
            points = 2
            points_multiple = points * value
            points_to_add = server_player_stats.points + points_multiple
            await server_player_stats.update(points=points_to_add)
        elif key == "headshots":
            points = 2
            points_multiple = points * value
            points_to_add = server_player_stats.points + points_multiple
            await server_player_stats.update(points=points_to_add)
        elif key == "deaths":
            points = -2
            points_multiple = (points * value) * -1
            points_to_remove = server_player_stats.points - points_multiple
            logger.info(points_to_remove)
            await server_player_stats.update(points=points_to_remove)
        await player_stats.update(**{key: old_value + value})
    return player_stats
"""

@router.post("/{server_id}/modules/chat-colors/")
async def create_player_chat_color(
    data: CreatePlayerChatColorSchema,
    server: Server = Depends(get_valid_server),
    chat_color_module_service: ChatColorModuleService = Depends(
        get_chat_color_module_service
    ),
    player_service: PlayerService = Depends(get_players_service),
):
    """
    Create player chat color
    :param data:
    :param chat_color_module_service:
    :param player:
    :param server:
    :return:
    """
    if data.steamid64:
        player = await get_valid_player_by_steamid(data.steamid64, player_service)
        return chat_color_module_service.create(
            server=server,
            player=player,
            tag=data.tag,
            tag_color=data.tag_color.as_hex(),
            name_color=data.name_color.as_hex(),
            text_color=data.text_color.as_hex(),
        )
    return await chat_color_module_service.create(
        server=server,
        tag=data.tag,
        tag_color=data.tag_color.as_hex(),
        name_color=data.name_color.as_hex(),
        text_color=data.text_color.as_hex(),
    )


@router.get("/{server_id}/modules/chat-colors/")
async def get_players_chat_colors(
    params: Params = Depends(),
    server: Server = Depends(get_valid_server),
    chat_color_module_service: ChatColorModuleService = Depends(
        get_chat_color_module_service
    ),
    player_service: PlayerService = Depends(get_players_service),
    flag: str | None = None,
    steamid64: str | None = None,
):
    """
    Get players chat colors
    :param flag:
    :param server:
    :param chat_color_module_service:
    :return:
    """
    if flag:
        return await chat_color_module_service.get_one(server=server, flag=flag)
    if steamid64:
        player = await get_valid_player_by_steamid(steamid64, player_service)
        return await chat_color_module_service.get_one(server=server, player=player)
    return await chat_color_module_service.get_all(server=server, params=params)


@router.put("/{server_id}/modules/chat-colors/{tag_id}")
async def update_player_chat_color(
    data: UpdatePlayerChatColorSchema,
    tag_id: int,
    server: Server = Depends(get_valid_server),
    chat_color_module_service: ChatColorModuleService = Depends(
        get_chat_color_module_service
    ),
    player_service: PlayerService = Depends(get_players_service),
):
    """
    Update player chat color
    :param tag_id:
    :param data:
    :param chat_color_module_service:
    :param server:
    :return:
    """
    chat_color_obj = await chat_color_module_service.get_one(id=tag_id, server=server)
    data_dict = data.dict()
    steamid64 = data_dict.get("steamid64", None)
    if steamid64:
        player = await get_valid_player_by_steamid(steamid64, player_service)
        data_dict.player = player
    validated_update_data = {}
    for item in data_dict.items():
        if item[1] is not None:
            validated_update_data[item[0]] = item[1]
    await chat_color_obj.update(**validated_update_data)
    return chat_color_obj
