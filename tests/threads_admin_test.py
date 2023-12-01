import pytest
from src.auth.schemas import RegisterUserSchema
from src.users.dependencies import get_users_service
from tests.conftest import (
    _get_auth_service,
    create_fake_categories,
    create_fake_threads,
    TEST_ADMIN_USER,
)

THREADS_ADMIN_ENDPOINT = "/v1/admin/forum/threads"


@pytest.mark.asyncio
async def test_unauthorized_admin_delete_thread(client):
    auth_service = await _get_auth_service()

    user = await auth_service.register(
        RegisterUserSchema(
            username="test",
            email="test@wp.pl",
            password="test123456",
            password2="test123456",
        ),
        is_activated=True,
    )

    categories = await create_fake_categories(1)
    threads = await create_fake_threads(1, user, categories[0])
    r = await client.delete(f"{THREADS_ADMIN_ENDPOINT}/{threads[0].id}")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_unauthorized_admin_update_thread(client):
    auth_service = await _get_auth_service()

    user = await auth_service.register(
        RegisterUserSchema(
            username="test",
            email="test@wp.pl",
            password="test123456",
            password2="test123456",
        ),
        is_activated=True,
    )

    categories = await create_fake_categories(1)
    threads = await create_fake_threads(1, user, categories[0])
    r = await client.put(f"{THREADS_ADMIN_ENDPOINT}/{threads[0].id}")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_admin_delete_thread(admin_client):
    users_service = await get_users_service()
    admin_user = await users_service.get_one(username=TEST_ADMIN_USER.get("username"))
    categories = await create_fake_categories(1)
    threads = await create_fake_threads(1, admin_user, categories[0])
    r = await admin_client.delete(f"{THREADS_ADMIN_ENDPOINT}/{threads[0].id}")
    assert r.status_code == 200
    assert r.json()["id"] == threads[0].id


@pytest.mark.asyncio
async def test_admin_close_thread(admin_client):
    users_service = await get_users_service()
    admin_user = await users_service.get_one(username=TEST_ADMIN_USER.get("username"))
    categories = await create_fake_categories(1)
    threads = await create_fake_threads(1, admin_user, categories[0])

    assert threads[0].is_closed is False
    r = await admin_client.post(f"{THREADS_ADMIN_ENDPOINT}/{threads[0].id}/close")
    assert r.status_code == 200
    assert r.json()["is_closed"] is True


@pytest.mark.asyncio
async def test_admin_open_thread(admin_client):
    users_service = await get_users_service()
    admin_user = await users_service.get_one(username=TEST_ADMIN_USER.get("username"))
    categories = await create_fake_categories(1)
    threads = await create_fake_threads(1, admin_user, categories[0])
    await threads[0].update(is_closed=True)
    assert threads[0].is_closed is True
    r = await admin_client.post(f"{THREADS_ADMIN_ENDPOINT}/{threads[0].id}/open")
    assert r.status_code == 200
    assert r.json()["is_closed"] is False


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data",
    [
        {"title": {"title": "New title"}},
        {"content": {"content": "New content"}},
        {
            "all": {
                "title": "New title",
                "content": "New content",
                "author": 1,
                "category": 1,
            }
        },
    ],
)
async def test_admin_update_thread(data, admin_client):
    users_service = await get_users_service()
    admin_user = await users_service.get_one(username=TEST_ADMIN_USER.get("username"))
    categories = await create_fake_categories(1)
    threads = await create_fake_threads(1, admin_user, categories[0])
    for _data in data:
        if _data == "title":
            r = await admin_client.put(
                f"{THREADS_ADMIN_ENDPOINT}/{threads[0].id}",
                json={"title": data[_data]["title"]},
            )
            assert r.status_code == 200
        elif _data == "content":
            r = await admin_client.put(
                f"{THREADS_ADMIN_ENDPOINT}/{threads[0].id}",
                json={"content": data[_data]["content"]},
            )
            assert r.status_code == 200
        elif _data == "all":
            r = await admin_client.put(
                f"{THREADS_ADMIN_ENDPOINT}/{threads[0].id}",
                json={
                    "title": data[_data]["title"],
                    "content": data[_data]["content"],
                    "author": data[_data]["author"],
                    "category": data[_data]["category"],
                },
            )
            assert r.status_code == 200
