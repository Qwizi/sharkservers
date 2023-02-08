from fastapi import APIRouter, Depends, Security
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.ormar import paginate
from ormar import NoMatch

from src.auth.dependencies import get_admin_user
from src.players.exceptions import SteamProfileNotFound, SteamProfileExists, InvalidSteamid
from src.players.models import Player
from src.players.schemas import steam_profile_out, CreateSteamProfile
from src.players.services import player_service
from src.players.utils import create_steam_profile
from src.users.models import User

router = APIRouter()


@router.get("", response_model=Page[steam_profile_out])
async def admin_get_steam_profiles(params: Params = Depends(),
                                   user: User = Security(get_admin_user, scopes=["players:all"])):
    steam_profiles = Player.objects
    return await paginate(steam_profiles, params)


@router.get("/{profile_id}", response_model=steam_profile_out)
async def admin_get_steam_profile(profile_id: int,
                                  user: User = Security(get_admin_user, scopes=["players:retrieve"])):
    try:
        steam_profile = await Player.objects.get(id=profile_id)
        return steam_profile
    except NoMatch:
        raise SteamProfileNotFound()


@router.post("", response_model=steam_profile_out)
async def admin_create_player(profile_data: CreateSteamProfile,
                              user: User = Security(get_admin_user, scopes=["players:create"])):
    player = await player_service.create_player(steamid64=profile_data.steamid64)
    return player


@router.delete("/{profile_id}", response_model=steam_profile_out)
async def admin_delete_steam_profile(profile_id: int,
                                     user: User = Security(get_admin_user, scopes=["players:delete"])):
    try:
        profile = await Player.objects.get(id=profile_id)
        await profile.delete()
        return profile
    except NoMatch:
        raise SteamProfileNotFound()
