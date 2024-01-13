"""Players models."""  # noqa: EXE002
from __future__ import annotations

import ormar

from sharkservers.db import BaseMeta, DateFieldsMixins


class SteamRepProfile(ormar.Model, DateFieldsMixins):
    """
    Represents a SteamRep profile.

    Attributes
    ----------
        id (int): The unique identifier of the profile.
        profile_url (str): The URL of the profile.
        is_scammer (bool): Indicates if the profile is a scammer.
        steamid64 (str): The 64-bit Steam ID of the profile.
    """

    class Meta(BaseMeta):
        """SteamRep profile metadata."""

        tablename = "steamrep_profiles"

    id: int = ormar.Integer(primary_key=True)  # noqa: A003
    profile_url: str | None = ormar.String(max_length=255, unique=True)
    is_scammer: bool | None = ormar.Boolean(default=False)
    steamid64: str | None = ormar.String(max_length=255, unique=True)


class Player(ormar.Model, DateFieldsMixins):
    """
    Represents a player in the game.

    Attributes
    ----------
        id (int): The unique identifier of the player.
        steamrep_profile (Optional[SteamRepProfile]): The player's SteamRep profile.
        username (str): The username of the player.
        steamid3 (str): The player's SteamID3.
        steamid32 (str): The player's SteamID32.
        steamid64 (str): The player's SteamID64.
        profile_url (str): The URL to the player's profile.
        avatar (str): The URL to the player's avatar.
        country_code (str): The country code of the player.
        reputation (int): The reputation score of the player.
    """

    class Meta(BaseMeta):
        """Player metadata."""

        tablename = "players"

    id: int = ormar.Integer(primary_key=True)  # noqa: A003
    steamrep_profile: SteamRepProfile | None = ormar.ForeignKey(
        SteamRepProfile,
        related_name="players",
    )
    username: str | None = ormar.String(max_length=32)
    steamid3: str | None = ormar.String(max_length=255, unique=True)
    steamid32: str | None = ormar.String(max_length=255, unique=True)
    steamid64: str | None = ormar.String(max_length=255, unique=True)
    profile_url: str | None = ormar.String(max_length=255, nullable=True, unique=True)
    avatar: str | None = ormar.String(max_length=255, nullable=True)
    country_code: str | None = ormar.String(max_length=15)
    reputation: int | None = ormar.Integer(default=1000)
