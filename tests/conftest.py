import asyncio
import random
from io import BytesIO
from unittest import mock

import pytest
import pytest_asyncio
import sqlalchemy
from PIL import ImageDraw, Image
from fastapi import File
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from httpx import AsyncClient

from src.auth.dependencies import (
    get_access_token_service,
    get_refresh_token_service,
)
from src.auth.schemas import RegisterUserSchema
from src.auth.services.auth import AuthService
from src.auth.views import limiter
from src.db import metadata, create_redis_pool
from src.forum.dependencies import get_categories_service, get_posts_service, get_threads_service, \
    get_thread_meta_service
from src.forum.enums import CategoryTypeEnum, ThreadStatusEnum
from src.forum.models import Category
from src.forum.schemas import CreateThreadSchema
from src.forum.services import CategoryService
from src.logger import logger
from src.main import app
from src.roles.dependencies import get_roles_service
from src.scopes.dependencies import get_scopes_service
from src.scopes.models import Scope
from src.servers.dependencies import get_servers_service
from src.services import MainService
from src.settings import get_settings
from src.users.dependencies import get_users_service
from src.users.models import User

DATABASE_URL = "sqlite:///../test.db"

TEST_USER = {
    "username": "User",
    "email": "test@test.pl",
    "password": "test123456",
}

TEST_ADMIN_USER = {
    "username": "Admin",
    "email": "admin@test.pl",
    "password": "test123456",
}

TEST_CATEGORY = {
    "name": "Test Category",
    "description": "Test Description",
    "type": CategoryTypeEnum.PUBLIC.value,
}

TEST_ROLE = {
    "name": "Test Role",
    "description": "Test Description",
    "color": "#000000",
}

TEST_SCOPE = {
    "app_name": "test_app",
    "value": "test_value",
    "description": "test_description",
    "protected": True,
}

TEST_THREAD = {
    "title": "Test Title",
    "content": "Test Content",
}

test_avatar_image_file = mock.MagicMock(file=File)
test_avatar_image_file.filename = "test_avatar.jpg"

settings = get_settings()


async def _get_auth_service():
    users_service = await get_users_service()
    roles_service = await get_roles_service()
    scopes_service = await get_scopes_service()
    auth_service = AuthService(
        users_service=users_service,
        roles_service=roles_service,
        scopes_service=scopes_service,
    )
    return auth_service


@pytest_asyncio.fixture(autouse=True, scope="function")
async def create_test_database():
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)
    roles_service = await get_roles_service()
    scopes_service = await get_scopes_service()
    auth_service = await _get_auth_service()
    await MainService.install(
        file_path=None,
        auth_service=auth_service,
        scopes_service=scopes_service,
        roles_service=roles_service,
        admin_user_data=RegisterUserSchema(
            username=TEST_ADMIN_USER.get("username"),
            email=TEST_ADMIN_USER.get("email"),
            password=TEST_ADMIN_USER.get("password"),
            password2=TEST_ADMIN_USER.get("password"),
        ),
        create_file=False,
    )
    yield
    metadata.drop_all(engine)


@pytest_asyncio.fixture(scope="module")
async def client():
    app.state.redis = await create_redis_pool()
    await FastAPILimiter.init(app.state.redis)

    override_limiter = RateLimiter(times=999, seconds=1)

    app.dependency_overrides[limiter] = override_limiter
    async with AsyncClient(app=app, base_url="http://localhost") as c:
        yield c

    app.dependency_overrides = {}


async def auth_user_headers(username, password):
    auth_service = await _get_auth_service()
    token, user = await auth_service.login(
        form_data=OAuth2PasswordRequestForm(
            username=username,
            password=password,
            scope="",
        ),
        jwt_access_token_service=await get_access_token_service(settings),
        jwt_refresh_token_service=await get_refresh_token_service(settings),
    )
    print(token)
    return {"Authorization": f"Bearer {token.access_token.token}"}


@pytest_asyncio.fixture(scope="function")
async def admin_client():
    headers = await auth_user_headers(
        TEST_ADMIN_USER.get("username"), TEST_ADMIN_USER.get("password")
    )
    app.state.redis = await create_redis_pool()
    await FastAPILimiter.init(app.state.redis)
    override_limiter = RateLimiter(times=999, seconds=1)
    app.dependency_overrides[limiter] = override_limiter
    async with AsyncClient(app=app, base_url="http://localhost", headers=headers) as c:
        yield c


@pytest_asyncio.fixture(scope="function")
async def logged_client():
    auth_service = await _get_auth_service()
    user = await auth_service.register(
        user_data=RegisterUserSchema(
            username=TEST_USER.get("username"),
            email=TEST_USER.get("email"),
            password=TEST_USER.get("password"),
            password2=TEST_USER.get("password"),
        ),
        is_activated=True,
    )
    headers = await auth_user_headers(user.username, TEST_USER.get("password"))
    logger.info(headers)
    app.state.redis = await create_redis_pool()
    await FastAPILimiter.init(app.state.redis)
    override_limiter = RateLimiter(times=9999, hours=1)
    app.dependency_overrides[limiter] = {"times": 999, "hours": 3}
    async with AsyncClient(app=app, base_url="http://localhost", headers=headers) as c:
        
        yield c
    app.dependency_overrides[limiter] = {}


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    yield loop


async def create_fake_users(number: int = 50):
    users_list = []
    auth_service = await _get_auth_service()
    for x in range(number):
        fake_user: User = await auth_service.register(
            user_data=RegisterUserSchema(
                username=f"test_user_{x}",
                email=f"test_user_{x}@test.pl",
                password="test_password",
                password2="test_password",
            )
        )
        users_list.append(fake_user)
    return users_list


async def create_fake_roles(number: int = 50, scopes: list[Scope] = None, is_staff: bool = False):
    roles_service = await get_roles_service()
    roles_list = []
    for role_id in range(number):
        role = await roles_service.create(
            name=f"test_role_{role_id}",
            color="#000000",
            is_staff=is_staff,
        )
        if scopes:
            for scope in scopes:
                await role.scopes.add(scope)
        roles_list.append(role)
    return roles_list


async def create_fake_categories(number: int = 50, category_type: CategoryTypeEnum = CategoryTypeEnum.PUBLIC.value):
    categories_service: CategoryService = await get_categories_service()
    categories_list: list[Category] = []
    for i in range(number):
        category_name = "Category " + str(i)
        category_description = "Category description " + str(i)
        category = await categories_service.create(
            name=category_name,
            description=category_description,
            type=category_type,
        )
        categories_list.append(category)
    return categories_list


async def create_fake_scopes(number: int, protected: bool = False) -> list[Scope]:
    scopes_service = await get_scopes_service()
    scopes_list = []
    app_name = "test_app"
    for i in range(number):
        scope_value = f"{app_name}_scope_{i}"
        scope_description = f"Scope description {i}"
        scope = await scopes_service.create(
            app_name=app_name,
            value=scope_value,
            description=scope_description,
            protected=protected,
        )
        scopes_list.append(scope)
    return scopes_list


async def create_fake_posts(number: int = 50, author: User = None, thread=None):
    posts_service = await get_posts_service()
    posts_list = []
    for i in range(number):
        post = await posts_service.create(
            content=f"Test content {i}",
            author=author,
        )
        posts_list.append(post)
        if thread:
            await thread.posts.add(post)
    return posts_list


async def create_fake_threads(
        number: int = 50,
        author: User = None,
        category: Category = None,
        status: ThreadStatusEnum = ThreadStatusEnum.PENDING.value,
        **kwargs
):
    threads_service = await get_threads_service()
    if category.type == CategoryTypeEnum.APPLICATION:
        servers_service = await get_servers_service()
        thread_meta_service = await get_thread_meta_service()
        server_exists = await servers_service.Meta.model.objects.filter(name="Test server").exists()
        if not server_exists:
            server = await servers_service.create(
                name="Test server",
                ip="127.0.0.1",
                port=25565,
            )
        else:
            server = await servers_service.get_one(name="Test server")
    threads_list = []
    for i in range(number):
        if category.type == CategoryTypeEnum.APPLICATION:
            threads_list.append(await threads_service.create_thread(
                data=CreateThreadSchema(
                    title=f"Test recrutation thread{i}",
                    content=f"Test content {i}",
                    author=author,
                    category=category.id,
                    server_id=server.id,
                    question_experience="Test question experience",
                    question_age="18",
                    question_reason="Test question why",
                ),
                author=author,
                category=category,
                thread_meta_service=thread_meta_service,
                servers_service=servers_service,
                status=status,
                **kwargs
            ))
        else:
            threads_list.append(await threads_service.create_thread(
                data=CreateThreadSchema(
                    title=f"Test title {i}",
                    content=f"Test content {i}",
                    author=author,
                    category=category.id,
                ),
                author=author,
                category=category,
                **kwargs
            ))
    return threads_list


def create_fake_image(image_format="PNG"):
    # Create a new image with a white background
    image = Image.new("RGB", (200, 200), "white")

    # Get the drawing context
    draw = ImageDraw.Draw(image)

    # Draw a red rectangle on the image
    rect_color = (255, 0, 0)  # Red color
    rect_position = (50, 50, 150, 150)  # Left, Upper, Right, Lower
    draw.rectangle(rect_position, fill=rect_color)

    # Save the image to a bytes-like object
    image_bytes = BytesIO()
    image.save(image_bytes, format=image_format)
    return image, image_bytes.getvalue()


def create_fake_invalid_image(additional_bytes: int = None):
    image, image_bytes = create_fake_image()

    if additional_bytes:
        image_bytes = BytesIO(b"\x00\x00\x00" + image_bytes[3:] * additional_bytes)
    else:
        image_bytes = BytesIO(b"\x00\x00\x00" + image_bytes[3:])
    return image_bytes.getvalue()


async def create_fake_servers(number: int = 50):
    servers_service = await get_servers_service()
    servers_list = []
    for i in range(number):
        random_ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
        random_port = int("".join(map(str, (random.randint(0, 5) for _ in range(4)))))
        servers_list.append(await servers_service.create(
            name=f"Test server {i}",
            ip=random_ip,
            port=random_port,
        ))
    return servers_list
