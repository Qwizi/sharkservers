from fastapi import APIRouter, Depends
from fastapi_pagination import Params

from src.players.dependencies import (
    get_players_service,
    get_valid_player_by_steamid,
)
from src.players.models import Player
from src.players.schemas import (
    CreatePlayerSchema,
    UpdatePlayerStatsSchema,
)
from src.players.services import (
    PlayerService,
)

router = APIRouter()


@router.get("")
async def get_players(
    params: Params = Depends(),
    players_service: PlayerService = Depends(get_players_service),
):
    return await players_service.get_all(params=params, related=["steamrep_profile"])


@router.post("")
async def create_player(
    player_data: CreatePlayerSchema,
    players_service: PlayerService = Depends(get_players_service),
    # app: App = Security(get_application, scopes=["players:create"]),
):
    """
    Create player
    :param app:
    :param player_data:
    :param players_service:
    :return:
    """
    player = await players_service.create_player(player_data.steamid64)
    return player


@router.get("/{steamid64}")
async def get_player(
    player: Player = Depends(get_valid_player_by_steamid),
):
    return player
