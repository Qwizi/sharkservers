import pytest

from src.auth.schemas import RegisterUserSchema
from src.users.dependencies import get_users_service
from tests.conftest import create_fake_threads, TEST_USER, create_fake_categories, TEST_THREAD, _get_auth_service

THREADS_ENDPOINT = "/v1/forum/threads"


@pytest.mark.asyncio
async def test_get_empty_threads(client):
    r = await client.get(THREADS_ENDPOINT)
    assert r.status_code == 200
    assert r.json()["total"] == 0


@pytest.mark.asyncio
async def test_get_threads(logged_client):
    users_service = await get_users_service()
    category = await create_fake_categories(1)
    author = await users_service.get_one(username=TEST_USER.get("username"))
    threads = await create_fake_threads(10, author, category[0])
    r = await logged_client.get(THREADS_ENDPOINT)
    assert r.status_code == 200
    assert r.json()["total"] == 10


@pytest.mark.asyncio
async def test_get_threads_with_category(logged_client):
    users_service = await get_users_service()
    category = await create_fake_categories(2)
    author = await users_service.get_one(username=TEST_USER.get("username"))
    # Create 10 threads in first category
    await create_fake_threads(10, author, category[0])
    # Create 5 threads in second category
    await create_fake_threads(5, author, category[1])

    r = await logged_client.get(f"{THREADS_ENDPOINT}?category={category[0].id}")
    assert r.status_code == 200
    assert r.json()["total"] == 10

    r2 = await logged_client.get(f"{THREADS_ENDPOINT}?category={category[1].id}")
    assert r2.status_code == 200
    assert r2.json()["total"] == 5


@pytest.mark.asyncio
async def test_get_thread_not_found(logged_client):
    r = await logged_client.get(f"{THREADS_ENDPOINT}/9999")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_unauthorized_create_thread(client):
    r = await client.post(THREADS_ENDPOINT)
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_create_thread(logged_client):
    categories = await create_fake_categories(1)
    r = await logged_client.post(THREADS_ENDPOINT, json={
        "title": TEST_THREAD.get("title"),
        "content": TEST_THREAD.get("content"),
        "category": categories[0].id
    })
    assert r.status_code == 200
    assert r.json()["title"] == TEST_THREAD.get("title")


@pytest.mark.asyncio
async def test_create_thread_with_invalid_category(logged_client):
    r = await logged_client.post(THREADS_ENDPOINT, json={
        "title": TEST_THREAD.get("title"),
        "content": TEST_THREAD.get("content"),
        "category": 999
    })
    assert r.status_code == 404


@pytest.mark.asyncio
@pytest.mark.parametrize("title", ["a", "a" * 65])
async def test_create_thread_with_invalid_title(title, logged_client):
    categories = await create_fake_categories(1)
    r = await logged_client.post(THREADS_ENDPOINT, json={
        "title": title,
        "content": TEST_THREAD.get("content"),
        "category": categories[0].id
    })
    assert r.status_code == 422


@pytest.mark.asyncio
@pytest.mark.parametrize("content", ["a"])
async def test_create_thread_with_invalid_content(content, logged_client):
    categories = await create_fake_categories(1)
    r = await logged_client.post(THREADS_ENDPOINT, json={
        "title": TEST_THREAD.get("title"),
        "content": content,
        "category": categories[0].id
    })
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_unauthorized_update_thread(client):
    auth_service = await _get_auth_service()
    user = await auth_service.register(
        RegisterUserSchema(
            username=TEST_USER.get("username"),
            email=TEST_USER.get("email"),
            password=TEST_USER.get("password"),
            password2=TEST_USER.get("password"),
        ), is_activated=True)
    category = await create_fake_categories(2)
    # Create 10 threads in first category
    threads = await create_fake_threads(10, user, category[0])
    r = await client.put(f"{THREADS_ENDPOINT}/{threads[0].id}")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_update_thread(logged_client):
    users_service = await get_users_service()
    category = await create_fake_categories(1)
    author = await users_service.get_one(username=TEST_USER.get("username"))
    threads = await create_fake_threads(1, author, category[0])
    old_title = threads[0].title
    old_content = threads[0].content
    new_title = "New title"
    new_content = "New content"
    r = await logged_client.put(f"{THREADS_ENDPOINT}/{threads[0].id}", json={
        "title": new_title,
        "content": new_content,
    })

    assert r.status_code == 200
    assert r.json()["title"] != old_title
    assert r.json()["content"] != old_content


@pytest.mark.asyncio
async def test_update_thread_where_author_is_not_same_like_logged_user(logged_client):
    auth_service = await _get_auth_service()
    new_user = await auth_service.register(
        RegisterUserSchema(
            username="new_user",
            email="new_user@email.pl",
            password="new_password123",
            password2="new_password123",
        ), is_activated=True)
    category = await create_fake_categories(1)
    threads = await create_fake_threads(1, new_user, category[0])
    r = await logged_client.put(f"{THREADS_ENDPOINT}/{threads[0].id}", json={
        "title": "New title",
        "content": "New content",
    })

    assert r.status_code == 400
