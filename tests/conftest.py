import asyncio
from asyncio import get_event_loop

import databases
import pytest
import pytest_asyncio
import sqlalchemy
from faker import Faker
from httpx import AsyncClient

from app.db import metadata
from app.main import app
from app.users.models import User

DATABASE_URL = "sqlite:///test.db"


@pytest.fixture(autouse=True, scope="function")
def create_test_database():
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)


@pytest_asyncio.fixture(scope="module")
async def client():
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
    for username in username_list:
        users_list.append(await User.objects.create(
            username=username,
            email=f"{username}@test.pl",
            password="test",
            avatar="asdasd"
        ))
    return users_list


TEST_USER = {
    "username": "Test user",
    "email": "test@test.pl",
    "password": "test",
    "avatar": "asdasd"
}
