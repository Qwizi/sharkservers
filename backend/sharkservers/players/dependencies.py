"""Players dependencies."""

from fastapi import Depends

from sharkservers.players.models import Player
from sharkservers.players.services import (
    PlayerService,
    SteamRepService,
)
from sharkservers.settings import Settings, get_settings


async def get_steamrep_service() -> SteamRepService:
    """
    Retrieve an instance of the SteamRepService class.

    Returns
    -------
        SteamRepService: An instance of the SteamRepService class.
    """
    return SteamRepService()


async def get_players_service(
    steamrep_service: SteamRepService = Depends(get_steamrep_service),
    settings: Settings = Depends(get_settings),
) -> PlayerService:
    """
    Retrieve the PlayerService instance with the specified dependencies.

    Args:
    ----
        steamrep_service (SteamRepService): The SteamRepService instance.
        settings (Settings): The Settings instance.

    Returns:
    -------
        PlayerService: The PlayerService instance.
    """
    return PlayerService(
        steamrep_service=steamrep_service,
        steam_api_key=settings.STEAM_API_KEY,
    )


async def get_valid_player(
    player_id: int,
    player_service: PlayerService = Depends(get_players_service),
) -> Player:
    """
    Retrieve a valid player by their ID.

    Args:
    ----
        player_id (int): The ID of the player.
        player_service (PlayerService, optional): The player service dependency. Defaults to Depends(get_players_service).

    Returns:
    -------
        Player: The valid player object.
    """
    return await player_service.get_one(
        id=player_id,
        select_related=["steamrep_profile"],
    )


async def get_valid_player_by_steamid(
    steamid64: str,
    player_service: PlayerService = Depends(get_players_service),
) -> Player:
    """
    Retrieve a valid player by their SteamID.

    Args:
    ----
        steamid64 (str): The SteamID of the player.
        player_service (PlayerService, optional): The player service dependency. Defaults to Depends(get_players_service).

    Returns:
    -------
        Player: The player object.
    """
    return await player_service.get_one(
        steamid64=steamid64,
        related=["steamrep_profile"],
    )
