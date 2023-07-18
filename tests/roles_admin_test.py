import json

import pytest

from src.scopes.dependencies import get_scopes_service
from src.scopes.services import ScopeService
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


@pytest.mark.asyncio
@pytest.mark.parametrize("is_staff", [True, False])
async def test_admin_create_role_without_scopes(is_staff, admin_client):
    r = await admin_client.post(ADMIN_ROLES_ENDPOINT, json={
        "name": TEST_ROLE.get("name"),
        "color": TEST_ROLE.get("color"),
        "is_staff": is_staff,
    })
    assert r.status_code == 200
    assert r.json()["name"] == TEST_ROLE["name"]
    assert r.json()["scopes"] == []


@pytest.mark.asyncio
async def test_admin_create_role_with_scopes(admin_client):
    scopes_service: ScopeService = await get_scopes_service()
    users_scopes = await scopes_service.get_all(app_name="users")
    users_scopes_ids = [scope.id for scope in await users_scopes.all()]
    r = await admin_client.post(ADMIN_ROLES_ENDPOINT, json={
        "name": TEST_ROLE.get("name"),
        "color": TEST_ROLE.get("color"),
        "is_staff": True,
        "scopes": users_scopes_ids,
    })
    assert r.status_code == 200
    assert r.json()["name"] == TEST_ROLE["name"]
    assert len(r.json()["scopes"]) == len(users_scopes_ids)
