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


@pytest.mark.asyncio
async def test_admin_get_scopes(admin_client):
    r = await admin_client.get("/admin/scopes")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_admin_get_scope(admin_client):
    r = await admin_client.get("/admin/scopes/1")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_admin_get_invalid_scope(admin_client):
    r = await admin_client.get("/admin/scopes/99999")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_admin_create_scope(admin_client):
    r = await admin_client.post(
        "/admin/scopes",
        json={"app_name": "test", "value": "test", "description": "test"},
    )
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_admin_delete_protected_scope(admin_client):
    r = await admin_client.delete("/admin/scopes/1")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_admin_delete_scope(admin_client):
    r = await admin_client.post(
        "/admin/scopes",
        json={
            "app_name": "test",
            "value": "test",
            "description": "test",
            "protected": False,
        },
    )
    assert r.status_code == 200

    r2 = await admin_client.delete(f"/admin/scopes/{r.json()['id']}")
    assert r2.status_code == 200
