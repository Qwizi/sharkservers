from pydantic import BaseModel

from app.steamprofile.models import SteamProfile

steam_profile_out = SteamProfile.get_pydantic(exclude={"user"})


class SteamPlayer(BaseModel):
    username: str
    steamid64: str
    steamid32: str
    steamid3: str
    profile_url: str
    avatar: str
    country_code: str
