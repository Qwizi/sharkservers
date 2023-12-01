from fastapi import Depends

from src.players.services import (
    SteamRepService,
    PlayerService,
)
from src.settings import Settings, get_settings


async def get_steamrep_service() -> SteamRepService:
    """
    Get steamrep service
    :return:
    """
    return SteamRepService()


async def get_players_service(
    steamrep_service: SteamRepService = Depends(get_steamrep_service),
    settings: Settings = Depends(get_settings),
) -> PlayerService:
    """
    Get players service
    :return:
    """
    return PlayerService(
        steamrep_service=steamrep_service, steam_api_key=settings.STEAM_API_KEY
    )


async def get_valid_player(
    player_id: int, player_service: PlayerService = Depends(get_players_service)
):
    """
    Get valid player
    :param player_id:
    :param player_service:
    :return:
    """
    return await player_service.get_one(
        id=player_id, select_related=["steamrep_profile"]
    )


async def get_valid_player_by_steamid(
    steamid64: str, player_service: PlayerService = Depends(get_players_service)
):
    """
    Get valid player
    :param steamid64:
    :param player_service:
    :return:
    """
    return await player_service.get_one(
        steamid64=steamid64, related=["steamrep_profile"]
    )


"""

async def get_player_stats_service():
    return PlayerStatsService()
"""
