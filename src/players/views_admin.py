from fastapi import APIRouter, Depends, Security
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Params
from ormar import NoMatch

from src.auth.dependencies import get_admin_user
from src.players.dependencies import get_players_service
from src.players.enums import PlayerEventEnum
from src.players.exceptions import (
    SteamProfileNotFound,
)
from src.players.models import Player
from src.players.schemas import steam_profile_out, CreatePlayerSchema
from src.players.services import PlayerService
from src.users.models import User

router = APIRouter()


@router.get("")
async def admin_get_steam_profiles(
    params: Params = Depends(),
    user: User = Security(get_admin_user, scopes=["players:all"]),
    players_service: PlayerService = Depends(get_players_service),
):
    return await players_service.get_all(params, related=["steamrep_profile"])


@router.get("/{profile_id}", response_model=steam_profile_out)
async def admin_get_steam_profile(
    profile_id: int, user: User = Security(get_admin_user, scopes=["players:retrieve"])
):
    try:
        steam_profile = await Player.objects.get(id=profile_id)
        return steam_profile
    except NoMatch:
        raise SteamProfileNotFound()


@router.post("")
async def admin_create_player(
    profile_data: CreatePlayerSchema,
    user: User = Security(get_admin_user, scopes=["players:create"]),
):
    dispatch(
        event_name=PlayerEventEnum.CREATE, payload={"steamid64": profile_data.steamid64}
    )
    return True


@router.delete("/{profile_id}", response_model=steam_profile_out)
async def admin_delete_steam_profile(
    profile_id: int, user: User = Security(get_admin_user, scopes=["players:delete"])
):
    try:
        profile = await Player.objects.get(id=profile_id)
        await profile.delete()
        return profile
    except NoMatch:
        raise SteamProfileNotFound()
