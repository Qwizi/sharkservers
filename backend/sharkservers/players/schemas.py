"""Schemas for the players module."""
from __future__ import annotations

from pydantic import BaseModel

from sharkservers.players.models import Player

player_out = Player.get_pydantic(exclude={})


class PlayerOut(player_out):
    """Player out schema."""


class SteamPlayer(BaseModel):
    """Steam player schema."""

    id: int | None = None
    username: str | None = None
    steamid64: str | None = None
    steamid32: str | None = None
    steamid3: str | None = None
    profile_url: str | None = None
    avatar: str | None = None
    country_code: str | None = None


class CreatePlayerSchema(BaseModel):
    """Create player schema."""

    steamid64: str
