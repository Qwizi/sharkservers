from typing import Optional

from pydantic import BaseModel

from shark_api.steamprofile.models import SteamProfile

steam_profile_out = SteamProfile.get_pydantic(exclude={"user"})


class SteamPlayer(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    steamid64: Optional[str] = None
    steamid32: Optional[str] = None
    steamid3: Optional[str] = None
    profile_url: Optional[str] = None
    avatar: Optional[str] = None
    country_code: Optional[str] = None


class CreateSteamProfile(BaseModel):
    steamid64: str
