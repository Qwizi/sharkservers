from fastapi import APIRouter, Depends, Security, BackgroundTasks
from fastapi_pagination import Page, Params
from ormar import NoMatch

from src.auth.dependencies import get_admin_user
from src.players.dependencies import get_players_service
from src.players.exceptions import (
    SteamProfileNotFound,
)
from src.players.models import Player
from src.players.schemas import PlayerOut, CreatePlayerSchema
from src.players.services import PlayerService
from src.users.models import User

router = APIRouter()


@router.get("")
async def admin_get_steam_profiles(
    params: Params = Depends(),
    user: User = Security(get_admin_user, scopes=["players:all"]),
    players_service: PlayerService = Depends(get_players_service),
) -> Page[PlayerOut]:
    return await players_service.get_all(params, related=["steamrep_profile"])


@router.get("/{profile_id}")
async def admin_get_steam_profile(
    profile_id: int, user: User = Security(get_admin_user, scopes=["players:retrieve"])
)  -> PlayerOut:
    try:
        steam_profile = await Player.objects.get(id=profile_id)
        return steam_profile
    except NoMatch:
        raise SteamProfileNotFound()


@router.post("")
async def admin_create_player(
    profile_data: CreatePlayerSchema,
    background_tasks: BackgroundTasks,
    user: User = Security(get_admin_user, scopes=["players:create"]),
    players_service: PlayerService = Depends(get_players_service),
):
    background_tasks.add_task(players_service.create_player, profile_data.dict()["steamid64"])
    return {"msg": "Player created"}


@router.delete("/{profile_id}")
async def admin_delete_steam_profile(
    profile_id: int, user: User = Security(get_admin_user, scopes=["players:delete"])
) -> PlayerOut:
    try:
        profile = await Player.objects.get(id=profile_id)
        await profile.delete()
        return profile
    except NoMatch:
        raise SteamProfileNotFound()
