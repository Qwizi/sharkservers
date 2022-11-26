import pytest
from httpx import AsyncClient
from ormar import NoMatch
from starlette.exceptions import HTTPException

from app.main import app
from app.users.exceptions import UserNotFound
from app.users.models import User
from app.users.schemas import UserOut
from tests.conftest import TEST_USER, create_50_fake_users


@pytest.mark.asyncio
async def test_users_list(client, faker):
    users_ = await create_50_fake_users(faker)
    response = await client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 50

    single_user = data[0]
    assert "password" not in single_user
    assert "email" not in single_user
    assert "username" is not None


@pytest.mark.asyncio
async def test_user_get(client, faker):
    users_ = await create_50_fake_users(faker)
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
