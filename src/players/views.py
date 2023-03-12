from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.ormar import paginate

from src.apps.models import App
from src.auth.dependencies import get_application
from src.players.dependencies import get_players_service, get_valid_player
from src.players.models import Player
from src.players.schemas import steam_profile_out, CreatePlayerSchema
from src.players.services import PlayerService
from src.players.utils import get_steam_user_info

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
    app: App = Security(get_application, scopes=["players:create"]),
):
    """
    Create player
    :param app:
    :param player_data:
    :param players_service:
    :return:
    """
    pass
    player = await players_service.create_player(player_data.steamid64)
    return player


@router.get("/{player_id}")
async def get_player(
    player: Player = Depends(get_valid_player),
):
    return player
