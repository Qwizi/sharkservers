import pytest
from jose import jwt

from src.auth.schemas import TokenSchema, RegisterUserSchema
from src.auth.services import auth_service
from src.roles.utils import create_default_roles
from src.scopes.utils import create_scopes
from src.settings import get_settings
from src.users.models import User
from tests.conftest import create_fake_users, TEST_USER

TEST_REGISTER_USER = {
    "username": "Test",
    "email": "test@test.pl",
    "password": "testpassword123",
    "password2": "testpassword123",
}

TEST_LOGIN_USER = {
    "username": TEST_REGISTER_USER["username"],
    "password": TEST_REGISTER_USER["password"],
}


@pytest.mark.asyncio
async def test_auth_register(client):
    r = await client.post("/auth/register", json=TEST_REGISTER_USER)
    assert r.status_code == 200
    assert len(await User.objects.all()) == 2
    assert r.json()["username"] == "Test"
    assert "password" not in r.json()
    assert r.json()["is_activated"] is False
    assert r.json()["is_superuser"] is False

    assert len(r.json()["roles"]) == 1
    assert r.json()["display_role"]["id"] == 2


@pytest.mark.asyncio
async def test_auth_register_exception_when_password_not_match(client):
    r = await client.post(
        "/auth/register",
        json={
            "username": TEST_REGISTER_USER["username"],
            "email": TEST_REGISTER_USER["email"],
            "password": TEST_REGISTER_USER["password"],
            "password2": "diffrentpassword",
        },
    )
    response_data = {
        "detail": [
            {
                "loc": ["body", "password2"],
                "msg": "Passwords do not match",
                "type": "value_error",
            }
        ]
    }

    assert r.status_code == 422
    assert r.json() == response_data


@pytest.mark.asyncio
async def test_auth_register_exception_when_username_or_password_is_taken(
    client,
):
    user = await auth_service.register(
        user_data=RegisterUserSchema(**TEST_REGISTER_USER)
    )
    r = await client.post(
        "/auth/register",
        json={
            "username": user.username,
            "email": user.email,
            "password": TEST_REGISTER_USER["password"],
            "password2": TEST_REGISTER_USER["password2"],
        },
    )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_auth_create_access_token(client):
    r = await client.post("/auth/register", json=TEST_REGISTER_USER)
    data = r.json()
    r = await client.post("/auth/token", data=TEST_LOGIN_USER)
    assert r.status_code == 200
    assert "access_token" in r.json()
    assert "refresh_token" in r.json()
    assert "token_type" in r.json()


@pytest.mark.asyncio
async def test_get_access_token_from_refresh_token(client, faker):
    await client.post("/auth/register", json=TEST_REGISTER_USER)
    r = await client.post("/auth/token", data=TEST_LOGIN_USER)
    token_data = r.json()

    r_r = await client.post(
        "/auth/token/refresh", json={"refresh_token": token_data["refresh_token"]}
    )
    assert r_r.status_code == 200


@pytest.mark.asyncio
async def test_logout_user(logged_client):
    r = await logged_client.get("/users/me")
    assert r.status_code == 200

    logout_r = await logged_client.post("/auth/logout")
    assert logout_r.status_code == 200

    r2 = await logged_client.get("/users/me")
    assert r2.status_code == 401
