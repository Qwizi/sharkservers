import pytest

from shark_api.steamprofile.utils import get_steam_user_info, create_steam_profile


def test_get_steam_user_info():
    steamid64 = "76561198190469450"
    steamid32 = "STEAM_1:0:115101861"
    info = get_steam_user_info(steamid64)
    assert info.steamid64 == steamid64
    assert info.steamid32 == steamid32


def test_get_steam_user_info_invalid_steamid64():
    steamid64 = "invalid"
    with pytest.raises(Exception) as e:
        info = get_steam_user_info(steamid64)
    assert e.value.args[0] == "Invalid steamid64"


@pytest.mark.asyncio
async def test_empty_get_steam_profiles(client):
    r = await client.get("/players")
    assert r.status_code == 200
    assert r.json()["total"] == 0


@pytest.mark.asyncio
async def test_get_steam_profiles(client):
    steamid64 = "76561198190469450"
    await create_steam_profile(steamid64)

    r = await client.get("/players")
    assert r.status_code == 200
    assert r.json()["total"] == 1
    assert r.json()["items"][0]["steamid64"] == steamid64
