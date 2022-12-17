from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, paginate
from steam.protobufs.steammessages_player_pb2 import Player

from app.steamprofile.models import SteamProfile
from app.steamprofile.schemas import SteamPlayer, steam_profile_out
from app.steamprofile.utils import get_steam_user_info

router = APIRouter()


@router.get("", response_model=Page[steam_profile_out])
async def get_steam_profiles():
    profiles = await SteamProfile.objects.select_related(["user", "user__display_role"]).all()
    return paginate(profiles)


@router.get("/info")
async def get_steam_player(steamid: str):
    try:
        return get_steam_user_info(steamid)
    except Exception:
        raise HTTPException(detail="Invalid steamid", status_code=400)
