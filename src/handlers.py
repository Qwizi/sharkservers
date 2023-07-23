import random

from fastapi_events.handlers.local import local_handler
from fastapi_events.typing import Event

from src.auth.dependencies import get_auth_service
from src.auth.schemas import RegisterUserSchema
from src.auth.services import AuthService
from src.enums import MainEventEnum
from src.logger import logger
from src.roles.dependencies import get_roles_service
from src.roles.services import RoleService
from src.settings import get_settings
from src.users.dependencies import get_users_service
from src.users.services import UserService

settings = get_settings()


def log_debug_event(event: Event):
    if settings.DEBUG:
        event_name, payload = event
        logger.debug(f"Event {event_name} with payload {payload}")


@local_handler.register(event_name="*")
async def handle_all_events_and_debug_log(event: Event):
    event_name, payload = event
    log_debug_event(event)


@local_handler.register(event_name=MainEventEnum.INSTALL)
async def handle_install_event(event: Event):
    pass


@local_handler.register(event_name="GENERATE_RANDOM_DATA")
async def generate_random_data(event: Event):
    logger.info("Generating random data")
    event_name, payload = event
    auth_service = payload.get("auth_service")
    categories_service = payload.get("categories_service")
    threads_service = payload.get("threads_service")
    users_list = []
    for i in range(100):
        new_user = await auth_service.register(
            user_data=RegisterUserSchema(
                username=f"TestUser{i}",
                password="test123456",
                password2="test123456",
                email=f"TestUser{i}@test.pl",
            )
        )
        users_list.append(new_user)
        logger.info(f"Created user {new_user.username}")

    categories_list = []
    for i in range(100):
        new_category = await categories_service.create(
            name=f"TestCategory{i}", description=f"Test description {i}"
        )
        categories_list.append(new_category)
        logger.info(f"Created category {new_category.name}")

    threads_list = []
    for i in range(1000):
        user = random.choice(list(users_list))
        category = random.choice(list(categories_list))
        new_thread = await threads_service.create(
            category=category,
            title=f"Test thread {i}",
            author=user,
            content="Test content {i}",
        )
        threads_list.append(new_thread)
        logger.info(f"Created thread {new_thread.title}")
