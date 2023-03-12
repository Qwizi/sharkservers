from typing import Optional

from pydantic import BaseModel

from src.players.models import Player

steam_profile_out = Player.get_pydantic(exclude={"user"})


class SteamPlayer(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    steamid64: Optional[str] = None
    steamid32: Optional[str] = None
    steamid3: Optional[str] = None
    profile_url: Optional[str] = None
    avatar: Optional[str] = None
    country_code: Optional[str] = None


class CreatePlayerSchema(BaseModel):
    steamid64: str
