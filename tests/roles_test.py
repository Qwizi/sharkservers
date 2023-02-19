import pytest

from src.roles.models import Role
from src.roles.utils import (
    create_default_roles,
    get_admin_role_scopes,
    get_user_role_scopes,
)
from src.scopes.models import Scope
from src.scopes.utils import create_scopes
from tests.conftest import create_fake_roles


@pytest.mark.asyncio
async def test_get_default_roles(client):
    await create_default_roles()
    r = await client.get("roles")
    assert r.status_code == 200
    data = r.json()
    assert len(data["items"]) == 3
    assert data["items"][0]["id"] == 1
    assert data["items"][1]["id"] == 2
    assert data["items"][2]["id"] == 3


@pytest.mark.asyncio
async def test_get_roles(client, faker):
    await create_default_roles()
    roles = await create_fake_roles(faker, 100)
    r = await client.get("roles")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 100 + 3


@pytest.mark.asyncio
async def test_get_role(client, faker):
    await create_default_roles()
    roles = await create_fake_roles(faker, 100)
    role = roles[2]
    r = await client.get(f"roles/{role.id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == role.id
    user_scopes = await get_user_role_scopes()
    assert len(data["scopes"]) == len(user_scopes)


@pytest.mark.asyncio
async def test_get_invalid_id_role(client):
    await create_default_roles()
    r = await client.get("roles/9555")
    assert r.status_code == 404
    assert r.json()["detail"] == "Role not found"


@pytest.mark.asyncio
@pytest.mark.parametrize("role_id", [1, 2, 3])
async def test_get_default_role(role_id, client):
    await create_default_roles()
    r = await client.get(f"roles/{role_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == role_id


@pytest.mark.asyncio
async def test_get_admin_role(client):
    admin_role_id = 1
    await create_scopes()
    await create_default_roles()
    r = await client.get(f"roles/{admin_role_id}")
    assert r.status_code == 200
    data = r.json()
    admin_scopes = await get_admin_role_scopes()
    assert len(data["scopes"]) == len(admin_scopes)


@pytest.mark.asyncio
async def test_get_user_role(client):
    user_role_id = 2
    await create_scopes()
    await create_default_roles()
    r = await client.get(f"roles/{user_role_id}")
    assert r.status_code == 200
    data = r.json()
    users_scopes = await get_user_role_scopes()
    assert len(data["scopes"]) == len(users_scopes)


@pytest.mark.asyncio
async def test_get_banned_role(client):
    banned_role_id = 3
    await create_scopes()
    await create_default_roles()
    r = await client.get(f"roles/{banned_role_id}")
    assert r.status_code == 200
    data = r.json()
    assert len(data["scopes"]) == 0


@pytest.mark.asyncio
@pytest.mark.skip
async def test_get_staff_roles(client):
    await create_scopes()
    await create_default_roles()
    r = await client.get("roles/staff")
    assert r.status_code == 200

    data = r.json()

    assert data["items"][0]["id"] == 1
