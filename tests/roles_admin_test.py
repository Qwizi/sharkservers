import pytest

from src.roles.models import Role
from tests.conftest import create_fake_roles

TEST_ROLE = {
    "name": "Test role",
    "color": "color",
    "scopes": [1, 2]
}


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


@pytest.mark.asyncio
async def test_admin_get_empty_roles(admin_client):
    r = await admin_client.get("/admin/roles")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_admin_get_roles(admin_client, faker):
    roles = await create_fake_roles(faker, number=50)

    r = await admin_client.get("/admin/roles")
    assert r.status_code == 200
    assert r.json()["total"] == 53


@pytest.mark.asyncio
async def test_admin_get_role(admin_client):
    r = await admin_client.get("/admin/roles/1")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_admin_get_invalid_role(admin_client):
    r = await admin_client.get("/admin/roles/9999")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_admin_create_role(admin_client):
    r = await admin_client.post("/admin/roles", json=TEST_ROLE)
    assert r.status_code == 200
    assert await Role.objects.count() == 4


@pytest.mark.asyncio
async def test_admin_delete_role(admin_client):
    r = await admin_client.post("/admin/roles", json=TEST_ROLE)
    assert r.status_code == 200
    data = r.json()

    r2 = await admin_client.delete(f"/admin/roles/{data['id']}")
    assert r2.status_code == 200


@pytest.mark.asyncio
async def test_admin_delete_invalid_role(admin_client):
    r = await admin_client.delete("/admin/roles/9999")
    assert r.status_code == 404


@pytest.mark.asyncio
@pytest.mark.parametrize("role_id", [1, 2, 3])
async def test_admin_delete_protected_roles(role_id, admin_client):
    r = await admin_client.delete(f"/admin/roles/{role_id}")
    assert r.status_code == 400
    assert r.json()["detail"] == "U cannot delete protected role"
