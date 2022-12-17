import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize("route", ["/admin/roles", "/admin/roles/999"])
async def test_unauthorized_admin_get_roles(route, client):
    r = await client.get(route)
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_unauthorized_admin_create_role(client):
    r = await client.post("/admin/roles")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_unauthorized_admin_delete_role(client):
    r = await client.delete("/admin/roles/1")
    assert r.status_code == 401
