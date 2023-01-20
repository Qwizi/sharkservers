from fastapi import APIRouter, Depends, Security
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.ormar import paginate
from ormar import NoMatch

from src.auth.dependencies import get_admin_user
from src.steamprofile.exceptions import SteamProfileNotFound, SteamProfileExists, InvalidSteamid
from src.steamprofile.models import SteamProfile
from src.steamprofile.schemas import steam_profile_out, CreateSteamProfile
from src.steamprofile.utils import create_steam_profile
from src.users.models import User

router = APIRouter()


@router.get("", response_model=Page[steam_profile_out])
async def admin_get_steam_profiles(params: Params = Depends(),
                                   user: User = Security(get_admin_user, scopes=["steamprofile:get_all"])):
    steam_profiles = SteamProfile.objects
    return await paginate(steam_profiles, params)


@router.get("/{profile_id}", response_model=steam_profile_out)
async def admin_get_steam_profile(profile_id: int,
                                  user: User = Security(get_admin_user, scopes=["steamprofile:retrieve"])):
    try:
        steam_profile = await SteamProfile.objects.get(id=profile_id)
        return steam_profile
    except NoMatch:
        raise SteamProfileNotFound()


@router.post("", response_model=steam_profile_out)
async def admin_create_steam_profile(profile_data: CreateSteamProfile,
                                     user: User = Security(get_admin_user, scopes=["steamprofile:create"])):
    profile_exists = await SteamProfile.objects.filter(steamid64=profile_data.steamid64).exists()
    if profile_exists:
        raise SteamProfileExists()
    try:
        profile = await create_steam_profile(profile_data.steamid64)
        return profile
    except Exception:
        raise InvalidSteamid()


@router.delete("/{profile_id}", response_model=steam_profile_out)
async def admin_delete_steam_profile(profile_id: int,
                                     user: User = Security(get_admin_user, scopes=["steamprofile:delete"])):
    try:
        profile = await SteamProfile.objects.get(id=profile_id)
        await profile.delete()
        return profile
    except NoMatch:
        raise SteamProfileNotFound()
