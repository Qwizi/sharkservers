from datetime import date
from typing import Optional

from pydantic import BaseModel

from src.players.models import Player

playerOut = Player.get_pydantic(exclude={
    
})

class PlayerOut(playerOut):
    pass

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


class UpdatePlayerStatsSchema(BaseModel):
    kills: Optional[int] = None
    deaths: Optional[int] = None
    assists: Optional[int] = None
    damage: Optional[int] = None
    damage_taken: Optional[int] = None
    healing: Optional[int] = None
    healing_taken: Optional[int] = None
    headshots: Optional[int] = None
    backstabs: Optional[int] = None
    dominations: Optional[int] = None
    revenges: Optional[int] = None
    captures: Optional[int] = None
    defends: Optional[int] = None
    ubers: Optional[int] = None
    teleports: Optional[int] = None
    suicides: Optional[int] = None
    sentries: Optional[int] = None
    buildings_destroyed: Optional[int] = None
    buildings_destroyed_sentry: Optional[int] = None
    buildings_destroyed_dispenser: Optional[int] = None
    buildings_destroyed_teleporter: Optional[int] = None
    time_played: Optional[int] = None
