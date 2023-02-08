from typing import Optional

import ormar

from src.db import DateFieldsMixins, BaseMeta
from src.servers.models import Server
from src.users.models import User


class SteamProfile(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "steamprofiles"

    id: int = ormar.Integer(primary_key=True)
    user: Optional[User] = ormar.ForeignKey(User, related_name="players")
    username: str = ormar.String(max_length=32)
    steamid3: str = ormar.String(max_length=255, unique=True)
    steamid32: str = ormar.String(max_length=255, unique=True)
    steamid64: str = ormar.String(max_length=255, unique=True)
    profile_url: str = ormar.String(max_length=255, nullable=True)
    avatar: str = ormar.String(max_length=255, nullable=True)
    country_code: str = ormar.String(max_length=15)


class Player(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "players"

    id: int = ormar.Integer(primary_key=True)
    steam_profile: Optional[SteamProfile] = ormar.ForeignKey(SteamProfile, related_name="players")
    server: Optional[Server] = ormar.ForeignKey(Server, related_name="players")
