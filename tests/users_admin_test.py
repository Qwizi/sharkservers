import pytest

from src.roles.enums import ProtectedDefaultRolesEnum
from src.users.models import User
from tests.conftest import create_fake_users, TEST_USER

ENDPOINT = "/v1/admin/users"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "route",
    [
        ENDPOINT,
        ENDPOINT + "/1",
    ],
)
async def test_unauthorized_admin_get_users(route, client):
    r = await client.get(route)
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_unauthorized_admin_create_user(client):
    r = await client.post(ENDPOINT)
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_unauthorized_admin_delete_user(client):
    r = await client.delete(ENDPOINT + "/1")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_unauthorized_admin_update_user(client):
    r = await client.put(ENDPOINT + "/1")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_admin_get_empty_users(admin_client):
    r = await admin_client.get(ENDPOINT)
    assert r.status_code == 200
    # Total 1 because of admin user
    assert r.json()["total"] == 1


@pytest.mark.asyncio
async def test_admin_get_users(admin_client):
    # Create 50 users
    await create_fake_users(number=50)
    r = await admin_client.get(ENDPOINT)
    assert r.status_code == 200
    # 51 because of admin user
    assert r.json()["total"] == 51
    assert r.json()["page"] == 1

    r2 = await admin_client.get(ENDPOINT + "?page=2&limit=25")
    assert r2.json()["items"][0] != r.json()["items"][0]
    assert r2.json()["page"] == 2


@pytest.mark.asyncio
async def test_admin_get_user(admin_client, faker):
    users = await create_fake_users(1)
    r = await admin_client.get(ENDPOINT + f"/{users[0].id}")
    assert r.status_code == 200
    assert r.json()["username"] == users[0].username


@pytest.mark.asyncio
async def test_admin_get_invalid_user(admin_client):
    r = await admin_client.get(ENDPOINT + "/999")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_admin_create_user_not_activated_and_no_superuser(admin_client):
    r = await admin_client.post(
        ENDPOINT,
        json={
            "username": TEST_USER.get("username"),
            "email": TEST_USER.get("email"),
            "password": TEST_USER.get("password"),
        },
    )
    assert r.status_code == 200
    assert r.json()["username"] == TEST_USER.get("username")
    assert await User.objects.count() == 2
    assert r.json()['is_activated'] is False
    assert r.json()['is_superuser'] is False
    assert "password" not in r.json()


@pytest.mark.asyncio
async def test_admin_create_user_activated_and_no_superuser(admin_client):
    r = await admin_client.post(
        ENDPOINT,
        json={
            "username": TEST_USER.get("username"),
            "email": TEST_USER.get("email"),
            "password": TEST_USER.get("password"),
            "is_activated": True,
        },
    )
    assert r.status_code == 200
    assert r.json()["username"] == TEST_USER.get("username")
    assert await User.objects.count() == 2
    assert r.json()['is_activated'] is True
    assert r.json()['is_superuser'] is False
    assert "password" not in r.json()


@pytest.mark.asyncio
async def test_admin_create_user_activated_and_superuser(admin_client):
    r = await admin_client.post(
        ENDPOINT,
        json={
            "username": TEST_USER.get("username"),
            "email": TEST_USER.get("email"),
            "password": TEST_USER.get("password"),
            "is_activated": True,
            "is_superuser": True,
        },
    )
    assert r.status_code == 200
    assert r.json()["username"] == TEST_USER.get("username")
    assert await User.objects.count() == 2
    assert r.json()['is_activated'] is True
    assert r.json()['is_superuser'] is True
    assert "password" not in r.json()


@pytest.mark.asyncio
async def test_admin_delete_invalid_user(admin_client):
    r = await admin_client.delete(ENDPOINT + "/9999")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_admin_delete_user(admin_client):
    users = await create_fake_users(1)
    r = await admin_client.delete(ENDPOINT + f"/{users[0].id}")
    assert r.status_code == 200
    assert await User.objects.count() == 1


@pytest.mark.asyncio
async def test_admin_update_invalid_user(admin_client):
    r = await admin_client.put(ENDPOINT + "/9999")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_admin_update_user_username(admin_client):
    users = await create_fake_users(1)
    updated_username = "updated_username"
    r = await admin_client.put(ENDPOINT + f"/{users[0].id}", json={"username": updated_username})
    assert r.status_code == 200
    assert r.json()["username"] == updated_username


@pytest.mark.asyncio
async def test_admin_update_user_email(admin_client):
    users = await create_fake_users(1)
    updated_email = "updated_email@test.pl"
    r = await admin_client.put(ENDPOINT + f"/{users[0].id}", json={"email": updated_email})
    assert r.status_code == 200
    assert r.json()["email"] == updated_email


@pytest.mark.asyncio
async def test_admin_update_user_invalid_display_role(admin_client):
    users = await create_fake_users(1)
    role_id = 9999
    r = await admin_client.put(ENDPOINT + f"/{users[0].id}", json={"display_role": role_id})
    assert r.status_code == 404


@pytest.mark.asyncio
@pytest.mark.parametrize("role", [
    ProtectedDefaultRolesEnum.ADMIN.value,
    ProtectedDefaultRolesEnum.USER.value,
    ProtectedDefaultRolesEnum.BANNED.value,
])
async def test_admin_update_user_display_role(role, admin_client):
    users = await create_fake_users(1)
    r = await admin_client.put(ENDPOINT + f"/{users[0].id}",
                               json={"display_role": role})
    assert r.status_code == 200
    assert r.json()["display_role"]["id"] == role


@pytest.mark.asyncio
@pytest.mark.parametrize("roles", [[22, 44], [28, 23, 21], [312, 433, 999]])
async def test_admin_update_user_invalid_roles(roles, admin_client):
    users = await create_fake_users(1)
    r = await admin_client.put(ENDPOINT + f"/{users[0].id}", json={"roles": roles})
    assert r.status_code == 404


@pytest.mark.asyncio
@pytest.mark.parametrize("roles", [
    [ProtectedDefaultRolesEnum.ADMIN.value],
    [ProtectedDefaultRolesEnum.USER.value],
    [ProtectedDefaultRolesEnum.BANNED.value],
    [ProtectedDefaultRolesEnum.ADMIN.value, ProtectedDefaultRolesEnum.USER.value],
    [ProtectedDefaultRolesEnum.ADMIN.value, ProtectedDefaultRolesEnum.BANNED.value],
    [ProtectedDefaultRolesEnum.USER.value, ProtectedDefaultRolesEnum.BANNED.value],
    [ProtectedDefaultRolesEnum.ADMIN.value, ProtectedDefaultRolesEnum.USER.value,
     ProtectedDefaultRolesEnum.BANNED.value]
])
async def test_admin_update_user_roles(roles, admin_client):
    users = await create_fake_users(1)
    r = await admin_client.put(ENDPOINT + f"/{users[0].id}", json={"roles": roles})
    assert r.status_code == 200
    assert len(r.json()["roles"]) == len(roles)
    roles_id = [role["id"] for role in r.json()["roles"]]
    assert all(role in roles_id for role in roles)
