import asyncio
import datetime
from unittest import mock
from zoneinfo import ZoneInfo

import pytest

from src.auth.enums import AuthExceptionsDetailEnum
from src.auth.schemas import RegisterUserSchema
from src.auth.utils import now_datetime
from src.roles.enums import ProtectedDefaultRolesEnum
from src.settings import get_settings
from src.users.models import User
from tests.conftest import create_fake_users, TEST_USER, _get_auth_service

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

REGISTER_ENDPOINT = "/v1/auth/register"
TOKEN_ENDPOINT = "/v1/auth/token"
REFRESH_TOKEN_ENDPOINT = "/v1/auth/token/refresh"
LOGOUT_ENDPOINT = "/v1/auth/logout"


@pytest.mark.asyncio
async def test_auth_register(client):
    r = await client.post(REGISTER_ENDPOINT, json=TEST_REGISTER_USER)
    assert r.status_code == 200
    assert len(await User.objects.all()) == 2
    assert r.json()["username"] == TEST_REGISTER_USER.get("username")
    assert "password" not in r.json()
    assert "secret_salt" not in r.json()
    assert r.json()["is_activated"] is False
    assert r.json()["is_superuser"] is False
    assert r.json()["display_role"]["id"] == ProtectedDefaultRolesEnum.USER.value


@pytest.mark.asyncio
async def test_auth_register_exception_when_password_not_match(client):
    r = await client.post(
        REGISTER_ENDPOINT,
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
    auth_service = await _get_auth_service()
    user = await auth_service.register(
        user_data=RegisterUserSchema(**TEST_REGISTER_USER)
    )
    r = await client.post(
        REGISTER_ENDPOINT,
        json={
            "username": user.username,
            "email": user.email,
            "password": TEST_REGISTER_USER["password"],
            "password2": TEST_REGISTER_USER["password2"],
        },
    )
    assert r.status_code == 422


@pytest.mark.asyncio
@pytest.mark.parametrize("username", [
    # too short
    "a",
    "bb",
    # too long
    "a" * 33,
    "b" * 34,
    # invalid characters
    "a!" * 3,
    "b@" * 3,
    "c#" * 3,
    "d$" * 3,
    "e%" * 3,
    "f^" * 3,
    "g&" * 3,
    "h*" * 3,
    # with spaces
    "Username with spaces",
])
async def test_auth_register_exception_with_invalid_username(username, client):
    r = await client.post(REGISTER_ENDPOINT, json={
        "username": username,
        "email": TEST_REGISTER_USER["email"],
        "password": TEST_REGISTER_USER["password"],
        "password2": TEST_REGISTER_USER["password2"],
    })
    assert r.status_code == 422


@pytest.mark.asyncio
@pytest.mark.parametrize("email", [
    # without @
    "email.pl",
    # without domain
    "email@",
    # without domain extension
    "email@domain",
])
async def test_auth_register_exception_with_invalid_email(email, client):
    r = await client.post(REGISTER_ENDPOINT, json={
        "username": TEST_REGISTER_USER["username"],
        "email": "email",
        "password": TEST_REGISTER_USER["password"],
        "password2": TEST_REGISTER_USER["password2"],
    })
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_auth_create_access_token(client):
    auth_service = await _get_auth_service()
    user = await auth_service.register(RegisterUserSchema(**TEST_REGISTER_USER), is_activated=True)
    r = await client.post(TOKEN_ENDPOINT, data={
        "username": user.username,
        "password": TEST_REGISTER_USER["password"],
    })
    assert r.status_code == 200
    assert r.json()["access_token"]["token"] is not None
    assert r.json()["access_token"]["exp"] is not None
    assert r.json()["refresh_token"]["token"] is not None
    assert r.json()["refresh_token"]["exp"] is not None
    assert r.json()["refresh_token"]["exp"] != r.json()["access_token"]["exp"]


@pytest.mark.asyncio
async def test_auth_create_access_token_exception_when_user_not_activated(client):
    auth_service = await _get_auth_service()
    user = await auth_service.register(RegisterUserSchema(**TEST_REGISTER_USER))
    r = await client.post(TOKEN_ENDPOINT, data={
        "username": user.username,
        "password": TEST_REGISTER_USER["password"],
    })

    assert r.status_code == 400
    assert r.json() == {"detail": AuthExceptionsDetailEnum.INACTIVE_USER.value}


@pytest.mark.asyncio
async def test_auth_create_access_token_exception_when_user_not_exist(client):
    # No user in database
    r = await client.post(TOKEN_ENDPOINT, data={
        "username": TEST_REGISTER_USER["username"],
        "password": TEST_REGISTER_USER["password"],
    })

    assert r.status_code == 404


@pytest.mark.asyncio
async def test_get_refresh_token(client):
    auth_service = await _get_auth_service()
    user = await auth_service.register(RegisterUserSchema(**TEST_REGISTER_USER), is_activated=True)
    token_response = await client.post(TOKEN_ENDPOINT, data=TEST_LOGIN_USER)
    assert token_response.status_code == 200
    token_data = token_response.json()
    await asyncio.sleep(1)
    refresh_token_response = await client.post(
        REFRESH_TOKEN_ENDPOINT, json={"refresh_token": token_data["refresh_token"]["token"]}
    )
    refresh_token_data = refresh_token_response.json()
    assert refresh_token_response.status_code == 200
    # refresh token should be different from access token
    assert token_data["access_token"]["token"] != refresh_token_data["access_token"]["token"]


@pytest.mark.asyncio
async def test_get_refresh_token_exception_when_refresh_token_not_exist(client):
    r = await client.post(REFRESH_TOKEN_ENDPOINT, json={"refresh_token": "test"})
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_get_refresh_token_exception_when_refresh_token_is_expired(client):
    auth_service = await _get_auth_service()
    settings = get_settings()
    user = await auth_service.register(RegisterUserSchema(**TEST_REGISTER_USER), is_activated=True)
    token_response = await client.post(TOKEN_ENDPOINT, data=TEST_LOGIN_USER)
    assert token_response.status_code == 200
    token_data = token_response.json()
    await asyncio.sleep(1)
    with mock.patch('src.auth.services.auth.now_datetime',
                    return_value=datetime.datetime.now(tz=ZoneInfo("Europe/Warsaw")) + datetime.timedelta(
                        minutes=settings.REFRESH_TOKEN_EXPIRES + 5)):
        refresh_token_response = await client.post(
            REFRESH_TOKEN_ENDPOINT, json={"refresh_token": token_data["refresh_token"]["token"]}
        )
        assert refresh_token_response.status_code == 401
        assert refresh_token_response.json() == {"detail": AuthExceptionsDetailEnum.TOKEN_EXPIRED.value}


@pytest.mark.asyncio
async def test_auth_exception_not_logged_client(client):
    r = await client.post(LOGOUT_ENDPOINT)
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_auth_logout(logged_client):
    r = await logged_client.post(LOGOUT_ENDPOINT)
    assert r.status_code == 200
