from fastapi import APIRouter, HTTPException, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.ormar import paginate

from src.steamprofile.models import SteamProfile
from src.steamprofile.schemas import SteamPlayer, steam_profile_out
from src.steamprofile.utils import get_steam_user_info

router = APIRouter()


@router.get("", response_model=Page[steam_profile_out])
async def get_steam_profiles(params: Params = Depends()):
    return await paginate(SteamProfile.objects.select_related(["user", "user__display_role"]), params)


@router.get("/info")
async def get_steam_player(steamid: str):
    try:
        return get_steam_user_info(steamid)
    except Exception:
        raise HTTPException(detail="Invalid steamid", status_code=400)
