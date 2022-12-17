import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize("route", ["/admin/players", "/admin/players/1"])
async def test_admin_get_steam_profiles(route, client):
    r = await client.get(route)
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_admin_create_steam_profile(client):
    r = await client.post("/admin/players")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_admin_delete_steam_profile(client):
    r = await client.delete("/admin/players/1")
    assert r.status_code == 401
