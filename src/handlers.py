import random

from fastapi_events.handlers.local import local_handler
from fastapi_events.typing import Event

from src.auth.schemas import RegisterUserSchema
from src.enums import MainEventEnum
from src.forum.enums import CategoryTypeEnum, ThreadStatusEnum
from src.logger import logger
from src.settings import get_settings

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
    posts_service = payload.get("posts_service")
    servers_service = payload.get("servers_service")

    async def generate_users(auth_service):
        users_list = []
        for i in range(10):
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
        return users_list

    async def generate_categories(categories_service, num: int = 10, type: CategoryTypeEnum = CategoryTypeEnum.PUBLIC):
        categories_list = []
        for i in range(num):
            name = f"TestCategory{i}" if type == CategoryTypeEnum.PUBLIC else f"TestApplicationCategory{i}"
            new_category = await categories_service.create(
                name=name, description=f"Test description {i}", type=type
            )
            categories_list.append(new_category)
            logger.info(f"Created category {new_category.name}")
        return categories_list
    
    async def generate_threads(threads_service, num=100, category=None, is_closed=False, is_pinned=False, status=ThreadStatusEnum.PENDING):
        threads_list = []
        for i in range(num):
            user = random.choice(list(users_list))
            category = random.choice(list(categories_list)) if not category else category
            kwargs = {}
            if category.type == CategoryTypeEnum.PUBLIC:
                kwargs["title"] = f"Test normal thread {i}"
                kwargs["content"] = f"Test normal content {i}"
            elif category.type == CategoryTypeEnum.APPLICATION:
                kwargs["server"] = random.choice(list(servers_list))
                kwargs["title"] = f"Test application thread {i}"
                kwargs["content"] = f"Test application content {i}"

            new_thread = await threads_service.create(
                    category=category,
                    author=user,
                    is_closed=is_closed,
                    is_pinned=is_pinned,
                    **kwargs
                )
            threads_list.append(new_thread)
            logger.info(f"Created thread {new_thread.title}")
        return threads_list
    
    async def generate_posts(posts_service, num=100):
        for i in range(num):
            user = random.choice(list(users_list))
            thread = random.choice(list(normal_threads_list))
            new_post = await posts_service.create(
                author=user,
                content=f"Test post {i}",
            )
            await thread.posts.add(new_post)
            logger.info(f"Created post {new_post.content}")

    async def generate_servers(servers_service, num=9):
        servers_list = []
        for i in range(num):
            server = await servers_service.create(
                ip="127.0.0.1",
                name=f"Test server {i}",
                port=i + 1
            )
            servers_list.append(server)
        return servers_list

    users_list = await generate_users(auth_service)
    servers_list = await generate_servers(servers_service)
    categories_list = await generate_categories(categories_service)
    application_categories_list = await generate_categories(categories_service=categories_service, num=2, type=CategoryTypeEnum.APPLICATION.value)
    normal_threads_list = await generate_threads(
        threads_service=threads_service
    )
    closed_threads_list = await generate_threads(
        threads_service=threads_service,
        num=5,
        category=None,
        is_closed=True
    )
    pinned_threads_list = await generate_threads(
        threads_service=threads_service,
        num=5,
        category=None,
        is_pinned=True
    )
    application_threads_list = await generate_threads(
        threads_service=threads_service,
        num=5,
        category=application_categories_list[0],
    )
    posts_list = await generate_posts(posts_service)

    logger.info("Finished generating random data")
