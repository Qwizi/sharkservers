from httpx import AsyncClient
import pytest
from src.enums import OrderEnum
from src.auth.schemas import RegisterUserSchema
from src.forum.dependencies import get_threads_service, get_thread_meta_service
from src.forum.enums import CategoryTypeEnum, ThreadStatusEnum
from src.users.dependencies import get_users_service
from tests.conftest import (
    create_fake_threads,
    TEST_USER,
    create_fake_categories,
    TEST_THREAD,
    _get_auth_service,
    create_fake_users,
    create_fake_servers,
)

THREADS_ENDPOINT = "/v1/forum/threads"


@pytest.mark.asyncio
async def test_get_empty_threads(client):
    r = await client.get(THREADS_ENDPOINT)
    assert r.status_code == 200
    assert r.json()["total"] == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "variants",
    [
        "default",
        "closed",
        "open",
        "by_category",
        # TODO: Implement these,
        ThreadStatusEnum.PENDING.value,
        ThreadStatusEnum.APPROVED.value,
        ThreadStatusEnum.REJECTED.value,
        OrderEnum.ID_DESC.value,
        OrderEnum.ID_ASC.value,
    ],
)
async def test_get_threads(variants, logged_client):
    users_service = await get_users_service()
    if variants == "default":
        category = await create_fake_categories(
            1, category_type=CategoryTypeEnum.PUBLIC
        )
        author = await users_service.get_one(username=TEST_USER.get("username"))
        threads = await create_fake_threads(10, author=author, category=category[0])
        r = await logged_client.get(THREADS_ENDPOINT)
        assert r.status_code == 200
        assert r.json()["total"] == 10
    elif variants == "closed":
        category = await create_fake_categories(
            1, category_type=CategoryTypeEnum.PUBLIC
        )
        author = await users_service.get_one(username=TEST_USER.get("username"))
        threads = await create_fake_threads(
            2, author=author, category=category[0], is_closed=True
        )
        r = await logged_client.get(THREADS_ENDPOINT + "?closed=true")
        assert r.status_code == 200
        assert r.json()["total"] == 2
        assert r.json()["items"][0]["is_closed"] is True
    elif variants == "open":
        category = await create_fake_categories(
            1, category_type=CategoryTypeEnum.PUBLIC
        )
        author = await users_service.get_one(username=TEST_USER.get("username"))
        await create_fake_threads(
            2, author=author, category=category[0], is_closed=False
        )
        r = await logged_client.get(THREADS_ENDPOINT + "?closed=false")
        assert r.status_code == 200
        assert r.json()["total"] == 2
        assert r.json()["items"][0]["is_closed"] is False
    elif variants == "by_category":
        category = await create_fake_categories(
            2, category_type=CategoryTypeEnum.PUBLIC
        )
        author = await users_service.get_one(username=TEST_USER.get("username"))
        await create_fake_threads(
            5,
            author=author,
            category=category[0],
        )
        await create_fake_threads(
            10,
            author=author,
            category=category[1],
        )
        r = await logged_client.get(THREADS_ENDPOINT + f"?category={category[0].id}")
        assert r.status_code == 200
        assert r.json()["total"] == 5
    elif variants == ThreadStatusEnum.PENDING.value:
        category = await create_fake_categories(
            1, category_type=CategoryTypeEnum.APPLICATION
        )
        author = await users_service.get_one(username=TEST_USER.get("username"))
        await create_fake_threads(
            10,
            author=author,
            category=category[0],
            status=ThreadStatusEnum.PENDING.value,
        )
        r = await logged_client.get(
            THREADS_ENDPOINT + f"?status={ThreadStatusEnum.PENDING.value}"
        )
        assert r.status_code == 200
        assert r.json()["total"] == 10

    elif variants == ThreadStatusEnum.APPROVED.value:
        category = await create_fake_categories(
            1, category_type=CategoryTypeEnum.APPLICATION
        )
        author = await users_service.get_one(username=TEST_USER.get("username"))
        await create_fake_threads(
            5,
            author=author,
            category=category[0],
            status=ThreadStatusEnum.PENDING.value,
        )
        await create_fake_threads(
            10,
            author=author,
            category=category[0],
            status=ThreadStatusEnum.APPROVED.value,
        )
        r = await logged_client.get(
            THREADS_ENDPOINT + f"?status={ThreadStatusEnum.APPROVED.value}"
        )
        assert r.status_code == 200
        assert r.json()["total"] == 10

    elif variants == ThreadStatusEnum.REJECTED.value:
        category = await create_fake_categories(
            1, category_type=CategoryTypeEnum.APPLICATION
        )
        author = await users_service.get_one(username=TEST_USER.get("username"))
        await create_fake_threads(
            5,
            author=author,
            category=category[0],
            status=ThreadStatusEnum.PENDING.value,
        )
        await create_fake_threads(
            10,
            author=author,
            category=category[0],
            status=ThreadStatusEnum.REJECTED.value,
        )
        r = await logged_client.get(
            THREADS_ENDPOINT + f"?status={ThreadStatusEnum.REJECTED.value}"
        )
        assert r.status_code == 200
        assert r.json()["total"] == 10
    elif variants == OrderEnum.ID_DESC.value:
        category = await create_fake_categories(
            1, category_type=CategoryTypeEnum.APPLICATION
        )
        author = await users_service.get_one(username=TEST_USER.get("username"))
        threads = await create_fake_threads(
            5,
            author=author,
            category=category[0],
            status=ThreadStatusEnum.PENDING.value,
        )
        first_thread_id = threads[0].id
        r = await logged_client.get(THREADS_ENDPOINT + f"?order={OrderEnum.ID_DESC}")
        assert r.status_code == 200
        assert r.json()["total"] == 5
        assert r.json()["items"][0]["id"] != first_thread_id

    elif variants == OrderEnum.ID_ASC.value:
        category = await create_fake_categories(
            1, category_type=CategoryTypeEnum.APPLICATION
        )
        author = await users_service.get_one(username=TEST_USER.get("username"))
        threads = await create_fake_threads(
            5,
            author=author,
            category=category[0],
            status=ThreadStatusEnum.PENDING.value,
        )
        first_thread_id = threads[0].id
        r = await logged_client.get(THREADS_ENDPOINT + f"?order={OrderEnum.ID_ASC}")
        assert r.status_code == 200
        assert r.json()["total"] == 5
        assert r.json()["items"][0]["id"] != 1


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
    r = await logged_client.post(
        THREADS_ENDPOINT,
        json={
            "title": TEST_THREAD.get("title"),
            "content": TEST_THREAD.get("content"),
            "category": categories[0].id,
        },
    )
    assert r.status_code == 200
    assert r.json()["title"] == TEST_THREAD.get("title")


@pytest.mark.asyncio
async def test_create_thread_with_invalid_category(logged_client):
    r = await logged_client.post(
        THREADS_ENDPOINT,
        json={
            "title": TEST_THREAD.get("title"),
            "content": TEST_THREAD.get("content"),
            "category": 999,
        },
    )
    assert r.status_code == 404


@pytest.mark.asyncio
@pytest.mark.parametrize("title", ["a", "a" * 65])
async def test_create_thread_with_invalid_title(title, logged_client):
    categories = await create_fake_categories(1)
    r = await logged_client.post(
        THREADS_ENDPOINT,
        json={
            "title": title,
            "content": TEST_THREAD.get("content"),
            "category": categories[0].id,
        },
    )
    assert r.status_code == 422


@pytest.mark.asyncio
@pytest.mark.parametrize("content", ["a"])
async def test_create_thread_with_invalid_content(content, logged_client):
    categories = await create_fake_categories(1)
    r = await logged_client.post(
        THREADS_ENDPOINT,
        json={
            "title": TEST_THREAD.get("title"),
            "content": content,
            "category": categories[0].id,
        },
    )
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
        ),
        is_activated=True,
    )
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
    r = await logged_client.put(
        f"{THREADS_ENDPOINT}/{threads[0].id}",
        json={
            "title": new_title,
            "content": new_content,
        },
    )

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
        ),
        is_activated=True,
    )
    category = await create_fake_categories(1)
    threads = await create_fake_threads(1, new_user, category[0])
    r = await logged_client.put(
        f"{THREADS_ENDPOINT}/{threads[0].id}",
        json={
            "title": "New title",
            "content": "New content",
        },
    )

    assert r.status_code == 400


@pytest.mark.asyncio
async def test_save_thread_signal():
    users = await create_fake_users(1)
    categories = await create_fake_categories(
        1, category_type=CategoryTypeEnum.APPLICATION.value
    )
    threads_service = await get_threads_service()
    threads_meta_service = await get_thread_meta_service()
    thread = await threads_service.create(
        title="Test title",
        content="Test content",
        category=categories[0],
        author=users[0],
    )
    server_id_name = "server_id"
    question_experience_name = "question_experience"
    question_age_name = "question_age"
    question_reason_name = "question_reason"

    meta_names = [
        server_id_name,
        question_experience_name,
        question_age_name,
        question_reason_name,
    ]
    for meta_name in meta_names:
        meta_field = await threads_meta_service.get_one(
            name=meta_name, thread_meta__id=thread.id
        )
        assert meta_field is not None
        assert meta_field.name == meta_name
        assert meta_field.value is None
    await thread.category.load()
    assert thread.category.threads_count == 1


@pytest.mark.asyncio
async def test_delete_thread_signal():
    users = await create_fake_users(1)
    categories = await create_fake_categories(
        1, category_type=CategoryTypeEnum.APPLICATION.value
    )
    category = categories[0]
    threads = await create_fake_threads(1, users[0], category)
    await category.load()
    assert category.threads_count == 1
    await threads[0].delete()
    await category.load()
    assert category.threads_count == 0


@pytest.mark.asyncio
async def test_create_application_thread(logged_client):
    categories = await create_fake_categories(
        1, category_type=CategoryTypeEnum.APPLICATION.value
    )
    servers = await create_fake_servers(1)
    server_id = servers[0].id
    question_experience = "Test experience"
    question_age = 18
    question_reason = "Test reason"

    r = await logged_client.post(
        THREADS_ENDPOINT,
        json={
            "title": TEST_THREAD.get("title"),
            "content": TEST_THREAD.get("content"),
            "category": categories[0].id,
            "server_id": server_id,
            "question_experience": question_experience,
            "question_age": question_age,
            "question_reason": question_reason,
        },
    )
    assert r.status_code == 200
    assert r.json()["title"] == TEST_THREAD.get("title")
    assert r.json()["content"] == TEST_THREAD.get("content")
    assert r.json()["category"]["id"] == categories[0].id
    for meta in r.json()["meta_fields"]:
        if meta["name"] == "server_id":
            assert meta["value"] == str(server_id)
        elif meta["name"] == "question_experience":
            assert meta["value"] == question_experience
        elif meta["name"] == "question_age":
            assert meta["value"] == str(question_age)
        elif meta["name"] == "question_reason":
            assert meta["value"] == question_reason
        else:
            assert False


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "meta_fields",
    [
        {
            # missing fields
        },
        {
            # invalid fields
            "server_id": "999",
            # invalid question_age
            "question_age": "invalid_age",
            "question_experience": 123,
            "question_reason": 123,
        },
        {
            # missing server_id
            "question_age": 18,
            "question_experience": "Test experience",
            "question_reason": "Test reason",
        },
        {
            # missing question_age
            "server_id": "999",
            "question_experience": "Test experience",
            "question_reason": "Test reason",
        },
        {
            # missing question_experience
            "server_id": "999",
            "question_age": 18,
            "question_reason": "Test reason",
        },
        {
            # missing question_reason
            "server_id": "999",
            "question_age": 18,
            "question_experience": "Test experience",
        },
    ],
)
async def test_create_application_thread_with_invalid_meta_fields(
    meta_fields, logged_client: AsyncClient
):
    categories = await create_fake_categories(
        1, category_type=CategoryTypeEnum.APPLICATION.value
    )

    r = await logged_client.post(
        THREADS_ENDPOINT,
        json={
            "title": TEST_THREAD.get("title"),
            "content": TEST_THREAD.get("content"),
            "category": categories[0].id,
            **meta_fields,
        },
    )
    assert r.status_code == 422
