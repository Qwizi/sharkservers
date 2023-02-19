import pytest

from src.users.models import User
from tests.conftest import create_fake_users, TEST_USER


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "route",
    [
        "/admin/users",
        "/admin/users/1",
    ],
)
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


@pytest.mark.asyncio
async def test_admin_get_empty_users(admin_client):
    r = await admin_client.get("/admin/users")
    assert r.status_code == 200
    assert r.json()["total"] == 1


@pytest.mark.asyncio
async def test_admin_get_users(admin_client, faker):
    users = await create_fake_users(faker, number=150)
    r = await admin_client.get("/admin/users")
    assert r.status_code == 200
    assert r.json()["total"] == 151
    assert r.json()["page"] == 1

    r2 = await admin_client.get("/admin/users?page=2")
    assert r2.json()["items"][0] != r.json()["items"][0]
    assert r2.json()["page"] == 2


@pytest.mark.asyncio
async def test_admin_get_user(admin_client, faker):
    users = await create_fake_users(faker, number=100)
    r = await admin_client.get(f"/admin/users/{users[50].id}")
    assert r.status_code == 200
    assert r.json()["username"] == users[50].username


@pytest.mark.asyncio
async def test_admin_get_invalid_user(admin_client):
    r = await admin_client.get("/admin/users/2")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_admin_create_user(admin_client):
    r = await admin_client.post(
        "/admin/users",
        json={
            "username": TEST_USER.get("username"),
            "email": TEST_USER.get("email"),
            "password": TEST_USER.get("password"),
            "is_activated": True,
            "display_role": 2,
        },
    )
    assert r.status_code == 200
    assert r.json()["username"] == TEST_USER.get("username")

    assert await User.objects.count() == 2


@pytest.mark.asyncio
async def test_admin_delete_user(admin_client, faker):
    users = await create_fake_users(faker, 1)
    assert await User.objects.count() == 2
    r = await admin_client.delete(f"/admin/users/{users[0].id}")
    assert r.status_code == 200
    assert await User.objects.count() == 1


@pytest.mark.asyncio
async def test_admin_delete_invalid_user(admin_client):
    r = await admin_client.delete("/admin/users/2")
    assert r.status_code == 404
