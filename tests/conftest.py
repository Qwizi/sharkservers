import asyncio
from asyncio import get_event_loop

import databases
import pytest
import pytest_asyncio
import sqlalchemy
from faker import Faker
from fastapi.security import OAuth2PasswordRequestForm
from httpx import AsyncClient

from src.logger import logger
from src.auth.dependencies import (
    get_access_token_service,
    get_refresh_token_service,
    get_auth_service,
)
from src.auth.schemas import RegisterUserSchema
from src.auth.utils import create_admin_user, _login_user, register_user
from src.db import metadata, get_redis, create_redis_pool
from src.forum.models import Category
from src.main import app
from src.roles.dependencies import get_roles_service
from src.roles.models import Role
from src.roles.utils import get_user_role_scopes, create_default_roles
from src.scopes.dependencies import get_scopes_service
from src.scopes.utils import create_scopes
from src.services import MainService
from src.settings import get_settings
from src.users.dependencies import get_users_service
from src.users.models import User

DATABASE_URL = "sqlite:///test.db"

TEST_USER = {
    "username": "Test user",
    "email": "test@test.pl",
    "password": "test",
}

TEST_ADMIN_USER = {
    "username": "Admin",
    "email": "admin@test.pl",
    "password": "admin",
}

settings = get_settings()


async def _get_auth_service():
    users_service = await get_users_service()
    roles_service = await get_roles_service()
    auth_service = await get_auth_service(
        users_service=users_service, roles_service=roles_service
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


"""
@pytest_asyncio.fixture(scope="module")
async def client():
    app.state.redis = await create_redis_pool()
    async with AsyncClient(app=app, base_url="http://localhost") as c:
        yield c


@pytest_asyncio.fixture(scope="function")
async def admin_client():
    await create_scopes()
    await create_default_roles()
    app.state.redis = await create_redis_pool()
    admin_user = await create_admin_user(
        user_data=RegisterUserSchema(
            username=TEST_ADMIN_USER.get("username"),
            email=TEST_ADMIN_USER.get("email"),
            password=TEST_ADMIN_USER.get("password"),
            password2=TEST_ADMIN_USER.get("password"),
        )
    )
    settings = get_settings()
    token, user = await _login_user(
        form_data=OAuth2PasswordRequestForm(
            username=admin_user.username,
            password=TEST_ADMIN_USER.get("password"),
            scope="",
        ),
        settings=settings,
    )
    headers = {"Authorization": f"Bearer {token.access_token}"}
    async with AsyncClient(app=app, base_url="http://localhost", headers=headers) as c:
        yield c
"""


@pytest_asyncio.fixture(scope="module")
async def client():
    app.state.redis = await create_redis_pool()
    async with AsyncClient(app=app, base_url="http://localhost") as c:
        yield c


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
    return {"Authorization": f"Bearer {token.access_token}"}


@pytest_asyncio.fixture(scope="function")
async def admin_client():
    headers = await auth_user_headers(
        TEST_ADMIN_USER.get("username"), TEST_ADMIN_USER.get("password")
    )
    app.state.redis = await create_redis_pool()
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
    async with AsyncClient(app=app, base_url="http://localhost", headers=headers) as c:
        yield c


"""

@pytest_asyncio.fixture(scope="function")
async def logged_client():
    await create_scopes()
    await create_default_roles()
    app.state.redis = await create_redis_pool()
    user = await register_user(
        user_data=RegisterUserSchema(
            username=TEST_USER.get("username"),
            email=TEST_USER.get("email"),
            password=TEST_USER.get("password"),
            password2=TEST_USER.get("password"),
        )
    )
    await user.update(is_activated=True)
    settings = get_settings()
    token, user = await _login_user(
        form_data=OAuth2PasswordRequestForm(
            username=user.username, password=TEST_USER.get("password"), scope=""
        ),
        settings=settings,
    )
    headers = {"Authorization": f"Bearer {token.access_token}"}
    async with AsyncClient(app=app, base_url="http://localhost", headers=headers) as c:
        yield c
"""


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    yield loop


@pytest.fixture(scope="session", autouse=True)
def faker_session_locale():
    return ["en_US"]


async def create_fake_users(number: int = 50):
    users_list = []
    auth_service = await _get_auth_service()
    for x in range(number):
        fake_user = await auth_service.register(
            user_data=RegisterUserSchema(
                username=f"test_user_{x}",
                email=f"test_user_{x}@test.pl",
                password="test_password",
                password2="test_password",
            )
        )
        users_list.append(fake_user)
    return users_list


async def create_fake_roles(faker: Faker, number: int = 50):
    roles_list = []
    role_name_list = set()
    while len(role_name_list) < number:
        role_name_list.add(faker.job())
    for role_name in role_name_list:
        role = await Role.objects.create(name=role_name, color="test_color")
        user_scopes = await get_user_role_scopes()
        for scope in user_scopes:
            await role.scopes.add(scope)
        roles_list.append(role)
    return roles_list


async def create_fake_categories(number: int = 50):
    categories_list = []
    for i in range(number):
        category_name = "Category " + str(i)
        category = await Category.objects.create(name=category_name)
        categories_list.append(category)
    return categories_list
