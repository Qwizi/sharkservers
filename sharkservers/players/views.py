"""Players views."""  # noqa: EXE002

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params

from sharkservers.players.dependencies import (
    get_players_service,
    get_valid_player_by_steamid,
)
from sharkservers.players.models import Player
from sharkservers.players.schemas import (
    CreatePlayerSchema,
    PlayerOut,
)
from sharkservers.players.services import (
    PlayerService,
)

router = APIRouter()


@router.get("")
async def get_players(
    params: Params = Depends(),  # noqa: B008
    players_service: PlayerService = Depends(get_players_service),  # noqa: B008
) -> Page[PlayerOut]:
    """
    Retrieve a list of players based on the provided parameters.

    Args:
    ----
        params (Params): The parameters for filtering and pagination.
        players_service (PlayerService): The service for retrieving player data.

    Returns:
    -------
        Page[PlayerOut]: A paginated list of player data.
    """
    return await players_service.get_all(params=params, related=["steamrep_profile"])


@router.post("")
async def create_player(
    player_data: CreatePlayerSchema,
    players_service: PlayerService = Depends(get_players_service),  # noqa: B008
) -> PlayerOut:
    """
    Create a new player.

    Args:
    ----
        player_data (CreatePlayerSchema): The data for creating a player.
        players_service (PlayerService): The service for managing players.

    Returns:
    -------
        PlayerOut: The created player.
    """
    return await players_service.create_player(player_data.steamid64)


@router.get("/{steamid64}")
async def get_player(
    player: Player = Depends(get_valid_player_by_steamid),  # noqa: B008
) -> PlayerOut:
    """
    Retrieve a player by their Steam ID.

    Args:
    ----
        player (Player): The player object obtained from the `get_valid_player_by_steamid` dependency.

    Returns:
    -------
        Player: The retrieved player object.

    """
    return player
