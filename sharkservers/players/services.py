"""Player services."""  # noqa: EXE002
from __future__ import annotations

import httpx
from fastapi import HTTPException
from steam.steamid import SteamID
from steam.webapi import WebAPI

from requests import HTTPError
from sharkservers.db import BaseService
from sharkservers.logger import logger
from sharkservers.players.exceptions import (
    player_not_found_exception,
)
from sharkservers.players.models import Player, SteamRepProfile
from sharkservers.players.schemas import SteamPlayer
from sharkservers.settings import get_settings

settings = get_settings()


class SteamRepService(BaseService):
    """
    Service for interacting with SteamRep API.

    Attributes
    ----------
        api_url (str): The URL to the SteamRep API.

    Methods
    -------
        get_data(steamid64: str) -> tuple[str, bool]: Get data from SteamRep API for a given steamid64.
        create_profile(steamid64: str) -> SteamRepProfile: Create a SteamRep profile for a given steamid64.

    """  # noqa: E501

    api_url = "https://steamrep.com/api/beta4/reputation/"

    class Meta:
        """SteamRep service metadata."""

        model = SteamRepProfile
        not_found_exception = None

    async def get_data(self, steamid64: str) -> tuple[str, bool]:
        """
        Get data from SteamRep API for a given steamid64.

        Args:
        ----
            steamid64 (str): The steamid64 of the player.

        Returns:
        -------
            tuple: A tuple containing the profile URL and a boolean indicating if the player is a scammer.
        """  # noqa: E501
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.api_url + steamid64 + "?json=1",
                timeout=20,
            )
            data = response.json()
            profile = data["steamrep"]["steamrepurl"]
            is_scammer = (
                data["steamrep"]["reputation"]["summary"] == "SCAMMER"
            )
            return profile, is_scammer

    async def create_profile(self, steamid64: str) -> SteamRepProfile:
        """
        Create a SteamRep profile for a given steamid64.

        Args:
        ----
            steamid64 (str): The steamid64 of the player.

        Returns:
        -------
            SteamRepProfile: The created SteamRep profile.
        """
        profile_created = await self.Meta.model.objects.filter(
            steamid64=steamid64,
        ).exists()
        if profile_created:
            raise HTTPException(
                detail="SteamRep profile already exists",
                status_code=401,
            )
        profile, is_scammer = await self.get_data(steamid64)
        return await self.create(
            profile_url=profile,
            is_scammer=is_scammer,
            steamid64=steamid64,
        )


class PlayerService(BaseService):
    """
    Service for interacting with Player data.

    Attributes
    ----------
        steam_api_key (str): The Steam API key.
        steam_api (WebAPI): The Steam API.
        steamrep_service (SteamRepService): The SteamRep service.

    Methods
    -------
        get_steam_player_info(steamid64: str) -> SteamPlayer: Get Steam player information for a given steamid64.
        create_player(steamid64: str) -> Player: Create a player with the given steamid64.
    """  # noqa: E501

    steam_api_key: str = None
    steam_api: WebAPI = None
    steamrep_service: SteamRepService

    class Meta:
        """Player service metadata."""

        model = Player
        not_found_exception = player_not_found_exception

    def __init__(self, steam_api_key: str, steamrep_service: SteamRepService) -> None:
        """Initialize the PlayerService."""
        self.steam_api_key = steam_api_key
        self.steamrep_service = steamrep_service

    def get_steam_player_info(self, steamid64: str) -> SteamPlayer:
        """
        Get Steam player information for a given steamid64.

        Args:
        ----
            steamid64 (str): The steamid64 of the player.

        Returns:
        -------
            SteamPlayer: The Steam player information.
        """
        try:
            steam_api = WebAPI(self.steam_api_key)
            results = steam_api.call(
                "ISteamUser.GetPlayerSummaries",
                steamids=steamid64,
            )
            logger.info(results)
            if not len(results["response"]["players"]):
                msg = "Invalid steamid64"
                raise Exception(msg)  # noqa: TRY002

            player = results["response"]["players"][0]

            profile_url = player["profileurl"]
            avatar = player["avatarfull"]
            loccountrycode = player.get("loccountrycode", "N/A")

            steamid64_from_player = player["steamid"]
            steamid32 = SteamID(steamid64_from_player).as_steam2
            steamid3 = SteamID(steamid64_from_player).as_steam3
            return SteamPlayer(
                username=player["personaname"],
                steamid64=steamid64_from_player,
                steamid32=steamid32,
                steamid3=steamid3,
                profile_url=profile_url,
                avatar=avatar,
                country_code=loccountrycode,
            )
        except HTTPError as e:
            logger.error(e)
            raise HTTPException(detail="Invalid steam api key", status_code=401) from e

    async def create_player(self, steamid64: str) -> Player:
        """
        Create a player with the given steamid64.

        Args:
        ----
            steamid64 (str): The steamid64 of the player.

        Returns:
        -------
            Player: The created player.
        """
        if await self.Meta.model.objects.filter(steamid64=steamid64).exists():
            raise HTTPException(detail="Player already exists", status_code=401)
        try:
            player_info = self.get_steam_player_info(steamid64)
            steamrep_profile = await self.steamrep_service.create_profile(steamid64)
            reputation = 1000
            if steamrep_profile.is_scammer:
                reputation = 800
            return await self.create(
                username=player_info.username,
                steamid64=player_info.steamid64,
                steamid32=player_info.steamid32,
                steamid3=player_info.steamid3,
                profile_url=player_info.profile_url,
                avatar=player_info.avatar,
                country_code=player_info.country_code,
                steamrep_profile=steamrep_profile,
                reputation=reputation,
            )
        except HTTPError as err:
            raise HTTPException(
                detail="Http error occurred while creating player",
                status_code=401,
            ) from err
