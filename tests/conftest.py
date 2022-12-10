import asyncio
from asyncio import get_event_loop

import databases
import pytest
import pytest_asyncio
import sqlalchemy
from faker import Faker
from httpx import AsyncClient

from app.db import metadata, get_redis, create_redis_pool
from app.main import app
from app.roles.models import Role
from app.roles.utils import get_user_role_scopes, create_default_roles
from app.scopes.utils import create_scopes
from app.users.models import User

DATABASE_URL = "sqlite:///test.db"

TEST_USER = {
    "username": "Test user",
    "email": "test@test.pl",
    "password": "test",
    "avatar": "asdasd"
}


@pytest.fixture(autouse=True, scope="function")
def create_test_database():
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)


@pytest_asyncio.fixture(scope="module")
async def client():
    app.state.redis = await create_redis_pool()
    async with AsyncClient(app=app, base_url="http://localhost") as c:
        yield c


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    yield loop


@pytest.fixture(scope='session', autouse=True)
def faker_session_locale():
    return ['pl_PL']


async def create_fake_users(faker: Faker, number: int = 50):
    username_list = set()
    while len(username_list) < number:
        username_list.add(faker.first_name().lower())
    users_list = []
    await create_scopes()
    await create_default_roles()
    user_role = await Role.objects.get(id=2)
    for username in username_list:
        user = await User.objects.create(
            username=username,
            email=f"{username}@test.pl",
            password="test",
            avatar="asdasd",
            display_role=user_role
        )
        await user.roles.add(user_role)
        users_list.append(user)
    return users_list


async def create_fake_roles(faker: Faker, number: int = 50):
    roles_list = []
    role_name_list = set()
    while len(role_name_list) < number:
        role_name_list.add(faker.job())
    for role_name in role_name_list:
        role = await Role.objects.create(
            name=role_name,
            color="test_color"
        )
        user_scopes = await get_user_role_scopes()
        for scope in user_scopes:
            role.scopes.add(scope)
        roles_list.append(role)
    return roles_list
