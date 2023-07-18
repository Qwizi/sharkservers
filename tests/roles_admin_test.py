import pytest

from tests.conftest import TEST_ROLE

ADMIN_ROLES_ENDPOINT = "/v1/admin/roles"


@pytest.mark.asyncio
async def test_unauthorized_get_roles(client):
    r = await client.get(ADMIN_ROLES_ENDPOINT)
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_unauthorized_get_role(client):
    r = await client.get(f"{ADMIN_ROLES_ENDPOINT}/1")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_unauthorized_create_role(client):
    r = await client.post(ADMIN_ROLES_ENDPOINT)
    assert r.status_code == 401


@pytest.mark.asyncio
@pytest.mark.skip
async def test_unauthorized_update_role(client):
    r = await client.put(f"{ADMIN_ROLES_ENDPOINT}/1")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_unauthorized_delete_role(client):
    r = await client.delete(f"{ADMIN_ROLES_ENDPOINT}/1")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_admin_get_default_roles(admin_client):
    r = await admin_client.get(ADMIN_ROLES_ENDPOINT)
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_admin_get_role(admin_client):
    r = await admin_client.get(f"{ADMIN_ROLES_ENDPOINT}/{TEST_ROLE['id']}")
    assert r.status_code == 200
    assert r.json()["name"] == TEST_ROLE["name"]
