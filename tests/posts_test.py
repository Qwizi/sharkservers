import pytest

from src.auth.schemas import RegisterUserSchema
from src.forum.dependencies import get_threads_service
from src.users.dependencies import get_users_service
from tests.conftest import create_fake_posts, create_fake_categories, create_fake_threads, TEST_USER, _get_auth_service

POSTS_ENDPOINT = "/v1/forum/posts"


@pytest.mark.asyncio
async def test_get_posts(logged_client):
    users_service = await get_users_service()
    author = await users_service.get_one(username=TEST_USER.get("username"))
    categories = await create_fake_categories(1)
    threads = await create_fake_threads(1, author, categories[0])
    posts = await create_fake_posts(10, author, threads[0])
    r = await logged_client.get(POSTS_ENDPOINT)
    assert r.status_code == 200
    assert r.json()["total"] == 10


@pytest.mark.asyncio
async def test_get_thread_posts(logged_client):
    users_service = await get_users_service()
    author = await users_service.get_one(username=TEST_USER.get("username"))
    categories = await create_fake_categories(1)
    threads = await create_fake_threads(2, author, categories[0])
    # Create 10 posts in first thread
    posts = await create_fake_posts(10, author, threads[0])
    # Create 5 posts in second thread
    posts = await create_fake_posts(5, author, threads[1])
    r = await logged_client.get(f"{POSTS_ENDPOINT}?thread_id={threads[0].id}")
    assert r.status_code == 200
    assert r.json()["total"] == 10
    r2 = await logged_client.get(f"{POSTS_ENDPOINT}?thread_id={threads[1].id}")
    assert r2.status_code == 200
    assert r2.json()["total"] == 5


@pytest.mark.asyncio
async def test_get_post_not_found(logged_client):
    r = await logged_client.get(f"{POSTS_ENDPOINT}/9999")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_get_post(logged_client):
    users_service = await get_users_service()
    author = await users_service.get_one(username=TEST_USER.get("username"))
    categories = await create_fake_categories(1)
    threads = await create_fake_threads(1, author, categories[0])
    posts = await create_fake_posts(1, author, threads[0])
    r = await logged_client.get(f"{POSTS_ENDPOINT}/{posts[0].id}")
    assert r.status_code == 200
    assert r.json()["id"] == posts[0].id


@pytest.mark.asyncio
async def test_unauthorized_create_post(client):
    r = await client.post(POSTS_ENDPOINT)
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_create_post_in_closed_thread(logged_client):
    users_service = await get_users_service()
    author = await users_service.get_one(username=TEST_USER.get("username"))
    categories = await create_fake_categories(1)
    threads = await create_fake_threads(1, author, categories[0])
    await threads[0].update(is_closed=True)
    r = await logged_client.post(POSTS_ENDPOINT, json={
        "thread_id": threads[0].id,
        "content": "test"
    })

    assert r.status_code == 400


@pytest.mark.asyncio
async def test_create_post(logged_client):
    users_service = await get_users_service()
    author = await users_service.get_one(username=TEST_USER.get("username"))
    categories = await create_fake_categories(1)
    threads = await create_fake_threads(1, author, categories[0])
    threads_service = await get_threads_service()
    r = await logged_client.post(POSTS_ENDPOINT, json={
        "thread_id": threads[0].id,
        "content": "test"
    })
    assert r.status_code == 200
    assert r.json()["content"] == "test"
    assert r.json()["author"]["id"] == author.id
    thread = await threads_service.get_one(id=threads[0].id, related=['posts'])
    assert len(thread.posts) == 1
    assert thread.posts[0].content == "test"


@pytest.mark.asyncio
async def test_unauthorized_update_post(client):
    auth_service = await _get_auth_service()
    author = await auth_service.register(
        RegisterUserSchema(
            username=TEST_USER.get("username"),
            email=TEST_USER.get("email"),
            password=TEST_USER.get("password"),
            password2=TEST_USER.get("password"),
        ), is_activated=True)
    categories = await create_fake_categories(1)
    threads = await create_fake_threads(1, author, categories[0])
    posts = await create_fake_posts(1, author, threads[0])
    r = await client.put(f"{POSTS_ENDPOINT}/{posts[0].id}")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_update_post_when_logged_client_is_not_a_author(logged_client):
    auth_service = await _get_auth_service()
    author = await auth_service.register(
        RegisterUserSchema(
            username="DifferentUser",
            email="test@email.pl",
            password=TEST_USER.get("password"),
            password2=TEST_USER.get("password"),
        ), is_activated=True)
    categories = await create_fake_categories(1)
    threads = await create_fake_threads(1, author, categories[0])
    posts = await create_fake_posts(1, author, threads[0])
    r = await logged_client.put(f"{POSTS_ENDPOINT}/{posts[0].id}")
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_update_post(logged_client):
    users_service = await get_users_service()
    author = await users_service.get_one(username=TEST_USER.get("username"))
    categories = await create_fake_categories(1)
    threads = await create_fake_threads(1, author, categories[0])
    posts = await create_fake_posts(1, author, threads[0])
    old_content = posts[0].content
    r = await logged_client.put(f"{POSTS_ENDPOINT}/{posts[0].id}", json={
        "content": "New content"
    })
    assert r.status_code == 200
    assert r.json()["content"] != old_content
    assert r.json()["author"]["id"] == author.id


@pytest.mark.asyncio
async def test_create_post_when_thread_is_closed(logged_client):
    users_service = await get_users_service()
    author = await users_service.get_one(username=TEST_USER.get("username"))
    categories = await create_fake_categories(1)
    threads = await create_fake_threads(1, author, categories[0])
    await threads[0].update(is_closed=True)
    r = await logged_client.post(POSTS_ENDPOINT, json={
        "thread_id": threads[0].id,
        "content": "test"
    })
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_get_post_likes(logged_client):
    users_service = await get_users_service()
    author = await users_service.get_one(username=TEST_USER.get("username"))
    categories = await create_fake_categories(1)
    threads = await create_fake_threads(1, author, categories[0])
    posts = await create_fake_posts(1, author, threads[0])
    r = await logged_client.get(f"{POSTS_ENDPOINT}/{posts[0].id}/likes")
    assert r.status_code == 200
    assert r.json()["total"] == 0


@pytest.mark.asyncio
@pytest.mark.parametrize("endpoint", [
    f"{POSTS_ENDPOINT}/1/like",
    f"{POSTS_ENDPOINT}/1/dislike",
])
async def test_unauthorized_like_and_dislike_post(endpoint, client):
    auth_service = await _get_auth_service()
    author = await auth_service.register(
        RegisterUserSchema(
            username="DifferentUser",
            email="test@email.pl",
            password=TEST_USER.get("password"),
            password2=TEST_USER.get("password"),
        ), is_activated=True)
    categories = await create_fake_categories(1)
    threads = await create_fake_threads(1, author, categories[0])
    posts = await create_fake_posts(1, author, threads[0])
    r = await client.post(endpoint)
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_like_post(logged_client):
    users_service = await get_users_service()
    author = await users_service.get_one(username=TEST_USER.get("username"))
    categories = await create_fake_categories(1)
    threads = await create_fake_threads(1, author, categories[0])
    posts = await create_fake_posts(1, author, threads[0])
    r = await logged_client.post(f"{POSTS_ENDPOINT}/{posts[0].id}/like")
    assert r.status_code == 200
    r2 = await logged_client.get(f"{POSTS_ENDPOINT}/{posts[0].id}/likes")
    assert r2.status_code == 200
    assert r2.json()["total"] == 1


@pytest.mark.asyncio
async def test_dislike_post(logged_client):
    users_service = await get_users_service()
    author = await users_service.get_one(username=TEST_USER.get("username"))
    categories = await create_fake_categories(1)
    threads = await create_fake_threads(1, author, categories[0])
    posts = await create_fake_posts(1, author, threads[0])
    # First like post
    r = await logged_client.post(f"{POSTS_ENDPOINT}/{posts[0].id}/like")
    assert r.status_code == 200
    # Then dislike post
    r2 = await logged_client.post(f"{POSTS_ENDPOINT}/{posts[0].id}/dislike")
    assert r2.status_code == 200
    # Check if post has 0 likes
    r3 = await logged_client.get(f"{POSTS_ENDPOINT}/{posts[0].id}/likes")
    assert r3.status_code == 200
    assert r3.json()["total"] == 0
