import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize("route", [
    "/admin/users",
    "/admin/users/1",
])
async def test_unauthorized_get_admin_users(route, client):
    r = await client.get(route)
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_unauthorized_admin_create_user(client):
    r = await client.post("/admin/users")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_unauthorized_admin_delete_user(client):
    r = await client.delete("/admin/users/1")
    assert r.status_code == 401
