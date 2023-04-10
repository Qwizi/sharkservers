import datetime
from typing import Optional

import ormar

from src.db import DateFieldsMixins, BaseMeta
from src.users.models import User


class SteamRepProfile(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "steamrep_profiles"

    id: int = ormar.Integer(primary_key=True)
    profile_url: str = ormar.String(max_length=255, unique=True)
    is_scammer: bool = ormar.Boolean(default=False)
    steamid64: str = ormar.String(max_length=255, unique=True)


class Player(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "players"

    id: int = ormar.Integer(primary_key=True)
    user: Optional[User] = ormar.ForeignKey(User, related_name="players")
    steamrep_profile: Optional[SteamRepProfile] = ormar.ForeignKey(
        SteamRepProfile, related_name="players"
    )
    username: str = ormar.String(max_length=32)
    steamid3: str = ormar.String(max_length=255, unique=True)
    steamid32: str = ormar.String(max_length=255, unique=True)
    steamid64: str = ormar.String(max_length=255, unique=True)
    profile_url: str = ormar.String(max_length=255, nullable=True, unique=True)
    avatar: str = ormar.String(max_length=255, nullable=True)
    country_code: str = ormar.String(max_length=15)
    reputation: int = ormar.Integer(default=1000)


class PlayerStats(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "player_stats"

    id: int = ormar.Integer(primary_key=True)
    kills: int = ormar.Integer(default=0)
    deaths: int = ormar.Integer(default=0)
    assists: int = ormar.Integer(default=0)
    damage: int = ormar.Integer(default=0)
    damage_taken: int = ormar.Integer(default=0)
    healing: int = ormar.Integer(default=0)
    healing_taken: int = ormar.Integer(default=0)
    headshots: int = ormar.Integer(default=0)
    backstabs: int = ormar.Integer(default=0)
    dominations: int = ormar.Integer(default=0)
    revenges: int = ormar.Integer(default=0)
    captures: int = ormar.Integer(default=0)
    defends: int = ormar.Integer(default=0)
    ubers: int = ormar.Integer(default=0)
    teleports: int = ormar.Integer(default=0)
    suicides: int = ormar.Integer(default=0)
    sentries: int = ormar.Integer(default=0)
    buildings_destroyed: int = ormar.Integer(default=0)
    buildings_destroyed_sentry: int = ormar.Integer(default=0)
    buildings_destroyed_dispenser: int = ormar.Integer(default=0)
    buildings_destroyed_teleporter: int = ormar.Integer(default=0)
    time_played: int = ormar.Integer(default=0)
    last_time_played: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    date: datetime.date = ormar.Date(default=datetime.date.today)
