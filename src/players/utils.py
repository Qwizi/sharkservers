from steam.steamid import SteamID
from steam.webapi import WebAPI

from src.settings import get_settings
from src.players.models import Player
from src.players.schemas import SteamPlayer

settings = get_settings()


def get_steam_user_info(steamid64: str) -> SteamPlayer:
    steam_api = WebAPI(settings.STEAM_API_KEY)
    results = steam_api.call('ISteamUser.GetPlayerSummaries', steamids=steamid64)
    if not len(results['response']['players']):
        raise Exception('Invalid steamid64')

    player = results['response']['players'][0]

    profile_url = player['profileurl']
    avatar = player['avatar']
    loccountrycode = player.get('loccountrycode', None)

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


async def create_steam_profile(steamid64: str) -> Player:
    player = get_steam_user_info(steamid64)
    steam_profile = await Player.objects.create(**player.dict())
    return steam_profile
