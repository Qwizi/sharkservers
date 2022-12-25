import pytest
from httpx import AsyncClient
from ormar import NoMatch
from starlette import status
from starlette.exceptions import HTTPException

from shark_api.auth.schemas import TokenSchema
from shark_api.main import app
from shark_api.roles.utils import create_default_roles
from shark_api.scopes.utils import create_scopes
from shark_api.users.exceptions import UserNotFound
from shark_api.users.models import User
from shark_api.users.schemas import UserOut
from tests.auth_test import TEST_REGISTER_USER, TEST_LOGIN_USER
from tests.conftest import TEST_USER, create_fake_users


@pytest.mark.asyncio
async def test_users_list(client, faker):
    users_ = await create_fake_users(faker, 50)
    response = await client.get("/users?size=25")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "page" in data
    assert "total" in data
    assert data['page'] == 1
    assert data['total'] == 50

    single_user = data['items'][0]
    assert "password" not in single_user
    assert "email" not in single_user
    assert "username" is not None


@pytest.mark.asyncio
async def test_users_list_pagination(client, faker):
    users_ = await create_fake_users(faker, 100)
    response = await client.get("/users?size=25")
    assert response.status_code == 200
    data = response.json()
    assert len(data['items']) == 25

    response2 = await client.get("/users?size=25&page=2")
    assert response2.status_code == 200
    data2 = response2.json()
    assert len(data2['items']) == 25
    assert data2['page'] == 2
    assert data != data2


@pytest.mark.asyncio
async def test_user_get(client, faker):
    users_ = await create_fake_users(faker)
    user_id = users_[0].id
    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 200
    single_user = response.json()
    assert single_user["id"] == user_id
    assert "password" not in single_user
    assert "email" not in single_user


@pytest.mark.asyncio
async def test_user_get_not_found(client):
    response = await client.get("/users/999")
    user_not_found = UserNotFound()
    assert response.status_code == user_not_found.status_code
    assert response.json()['detail'] == user_not_found.detail


@pytest.mark.asyncio
async def test_get_unactivated_logged_user(client):
    await create_scopes()
    await create_default_roles()
    register_r = await client.post("/auth/register", json=TEST_REGISTER_USER)
    token_r = await client.post("/auth/token", data=TEST_LOGIN_USER)
    access_token = token_r.json()['access_token']
    r = await client.get("/users/me", headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_logged_user(logged_client):
    r = await logged_client.get("/users/me")
    assert r.status_code == status.HTTP_200_OK
    assert r.json()['username'] == TEST_USER.get('username')
    assert r.json()['is_activated'] is True
    assert r.json()['is_superuser'] is False
    assert "roles" in r.json()
    assert "display_role" in r.json()


@pytest.mark.asyncio
async def test_change_logged_user_username(logged_client):
    change_username_r = await logged_client.post("/users/me/username", json={"username": "New username"})
    assert change_username_r.status_code == status.HTTP_200_OK
    assert change_username_r.json()["username"] != TEST_USER.get("username")
    assert change_username_r.json()["username"] == "New username"


@pytest.mark.asyncio
async def test_change_logged_user_username_unauthenticated(client):
    r = await client.post("users/me/username", json={"username": "New username"})
    assert r.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_last_logged_users(client):
    await create_scopes()
    await create_default_roles()

    register_r = await client.post("/auth/register", json=TEST_REGISTER_USER)
    user = await User.objects.get(username=TEST_LOGIN_USER['username'])
    await user.update(is_activated=True)
    assert user.is_activated is True
    token_r = await client.post("/auth/token", data=TEST_LOGIN_USER)

    online_users_r = await client.get("/users/online")
    assert online_users_r.status_code == status.HTTP_200_OK
    assert online_users_r.json()["total"] == 1
