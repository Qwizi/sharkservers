import pytest

from app.users.models import User
from tests.conftest import create_fake_users

TEST_USER = {
    "username": "Test",
    "email": "test@test.pl",
    "password": "testpassword123",
    "password2": "testpassword123"
}


@pytest.mark.asyncio
async def test_auth_register(client):
    r = await client.post("/auth/register", json=TEST_USER)
    assert r.status_code == 200
    assert len(await User.objects.all()) == 1
    assert r.json()['username'] == "Test"
    assert "password" not in r.json()
    assert r.json()["is_activated"] is False
    assert r.json()["is_superuser"] is False


@pytest.mark.asyncio
async def test_auth_register_exception_when_password_not_match(client):
    TEST_USER["password2"] = "diffrentpassword"
    r = await client.post("/auth/register", json=TEST_USER)
    response_data = {
        "detail": [
            {
                'loc': ['body', 'password2'], 'msg': 'Passwords do not match', 'type': 'value_error'
            }
        ]
    }

    assert r.status_code == 422
    assert r.json() == response_data


@pytest.mark.asyncio
async def test_auth_register_exception_when_username_or_password_is_taken(client, faker):
    users = await create_fake_users(faker, 1)
    user = users[0]
    r = await client.post("/auth/register", json={
        "username": user.username,
        "email": user.email,
        "password": TEST_USER['password'],
        "password2": TEST_USER['password']
    })
    assert r.status_code == 422
    assert r.json()["detail"] == "Email or username already exists"
