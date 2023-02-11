import httpx
from bs4 import BeautifulSoup
from steam.steamid import SteamID
from steam.webapi import WebAPI

from src.db import BaseService
from src.players.models import SteamRepProfile, Player
from src.players.schemas import SteamPlayer
from src.settings import get_settings

settings = get_settings()


class SteamRepService(BaseService):
    api_url = "https://steamrep.com/api/beta4/reputation/"

    async def get_data(self, steamid64: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.api_url + steamid64 + "?json=1", timeout=20)
            data = response.json()
            profile = data['steamrep']['steamrepurl']
            is_scammer = True if data['steamrep']['reputation']['summary'] == 'SCAMMER' else False
            return profile, is_scammer

    async def create_profile(self, steamid64: str):
        profile, is_scammer = await self.get_data(steamid64)
        return await self.create(
            profile_url=profile,
            is_scammer=is_scammer
        )


class PlayerService(BaseService):
    steam_api_key: str = None
    steam_api: WebAPI = None
    steam_rep_service: SteamRepService

    def __init__(self, model, not_found_exception, steam_api_key, steamrep_service):
        self.super = super().__init__(model, not_found_exception)
        self.steam_api_key = steam_api_key
        self.steam_api = WebAPI(self.steam_api_key)
        self.steam_rep_service = steamrep_service

    def get_steam_player_info(self, steamid64: str) -> SteamPlayer:
        steam_api = WebAPI(self.steam_api_key)
        results = steam_api.call('ISteamUser.GetPlayerSummaries', steamids=steamid64)
        if not len(results['response']['players']):
            raise Exception('Invalid steamid64')

        player = results['response']['players'][0]

        profile_url = player['profileurl']
        avatar = player['avatar']
        loccountrycode = player.get('loccountrycode', "N/A")

        steamid64_from_player = player['steamid']
        steamid32 = SteamID(steamid64_from_player).as_steam2
        steamid3 = SteamID(steamid64_from_player).as_steam3
        return SteamPlayer(
            username=player['personaname'],
            steamid64=steamid64_from_player,
            steamid32=steamid32,
            steamid3=steamid3,
            profile_url=profile_url,
            avatar=avatar,
            country_code=loccountrycode
        )

    async def create_player(self, steamid64: str) -> Player:
        player_info = self.get_steam_player_info(steamid64)
        steamrep_profile = await self.steam_rep_service.create_profile(steamid64)
        reputation = 1000
        if steamrep_profile.is_scammer:
            reputation = 800
        player = await self.create(
            username=player_info.username,
            steamid64=player_info.steamid64,
            steamid32=player_info.steamid32,
            steamid3=player_info.steamid3,
            profile_url=player_info.profile_url,
            avatar=player_info.avatar,
            country_code=player_info.country_code,
            steamrep_profile=steamrep_profile,
            reputation=reputation
        )
        return player


steamrep_profile_service = SteamRepService(model=SteamRepProfile, not_found_exception=None)
player_service = PlayerService(model=Player, not_found_exception=None, steam_api_key=settings.STEAM_API_KEY,
                               steamrep_service=steamrep_profile_service)
