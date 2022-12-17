import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize("route", ["/admin/scopes", "/admin/scopes/1"])
async def test_unauthorized_admin_get_scopes(route, client):
    r = await client.get(route)
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_unauthorized_admin_create_scope(client):
    r = await client.post("/admin/scopes")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_unauthorized_admin_delete_scope(client):
    r = await client.delete("/admin/scopes/1")
    assert r.status_code == 401
