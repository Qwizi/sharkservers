from fastapi import Depends

from src.players.services import SteamRepService, PlayerService
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
