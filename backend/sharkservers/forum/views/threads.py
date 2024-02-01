"""Threads views."""
from fastapi import APIRouter, Depends, Security
from fastapi_limiter.depends import RateLimiter
from fastapi_pagination import Page, Params

from sharkservers.auth.dependencies import get_current_active_user
from sharkservers.forum.dependencies import (
    get_categories_service,
    get_thread_meta_service,
    get_threads_service,
    get_valid_thread,
    get_valid_thread_with_author,
)
from sharkservers.forum.enums import ThreadStatusEnum
from sharkservers.forum.models import Thread
from sharkservers.forum.schemas import (
    CreateThreadSchema,
    ThreadOut,
    ThreadQuery,
    UpdateThreadSchema,
)
from sharkservers.forum.services import (
    CategoryService,
    ThreadMetaService,
    ThreadService,
)
from sharkservers.servers.dependencies import get_servers_service
from sharkservers.servers.services import ServerService
from sharkservers.settings import get_settings
from sharkservers.users.models import User

router = APIRouter()

settings = get_settings()

limiter = RateLimiter(
    times=999 if settings.TESTING else 5,
    minutes=60 if settings.TESTING else 2,
)


@router.get("")
async def get_threads(
    params: Params = Depends(),
    queries: ThreadQuery = Depends(),
    threads_service: ThreadService = Depends(get_threads_service),
) -> Page[ThreadOut]:
    """
    Get all threads.

    Args:
    ----
        params (Params, optional): The params. Defaults to Depends().
        queries (ThreadQuery, optional): The queries. Defaults to Depends().
        threads_service (ThreadService, optional): The threads service. Defaults to Depends(get_threads_service).

    Returns:
    -------
        Page[ThreadOut]: The threads.
    """
    kwargs = {}
    if queries.category:
        kwargs["category__id"] = queries.category
    if queries.order_by:
        if queries.category:
            kwargs["order_by"] = ["-is_pinned", queries.order_by]
        else:
            kwargs["order_by"] = queries.order_by
    if queries.server:
        kwargs["server__id"] = queries.server
    if queries.status:
        kwargs["status"] = queries.status
    if queries.closed is not None:
        kwargs["is_closed"] = queries.closed

    return await threads_service.get_all(
        params=params,
        related=[
            "category",
            "author",
            "author__display_role",
            "author__player",
            "author__player__steamrep_profile",
            "meta_fields",
            "server",
            "server__admin_role",
        ],
        **kwargs,
    )


@router.post("", dependencies=[Depends(limiter)])
async def create_thread(  # noqa: PLR0913
    thread_data: CreateThreadSchema,
    user: User = Security(get_current_active_user, scopes=["threads:create"]),
    threads_service: ThreadService = Depends(get_threads_service),
    categories_service: CategoryService = Depends(get_categories_service),
    thread_meta_service: ThreadMetaService = Depends(get_thread_meta_service),
    servers_service: ServerService = Depends(get_servers_service),
) -> ThreadOut:
    """
    Create thread.

    Args:
    ----
        thread_data (CreateThreadSchema): The thread data.
        user (User, optional): The user. Defaults to Security(get_current_active_user, scopes=["threads:create"]).
        threads_service (ThreadService, optional): The threads service. Defaults to Depends(get_threads_service).
        categories_service (CategoryService, optional): The categories service. Defaults to Depends(get_categories_service).
        thread_meta_service (ThreadMetaService, optional): The thread meta service. Defaults to Depends(get_thread_meta_service).
        servers_service (ServerService, optional): The servers service. Defaults to Depends(get_servers_service).


    Returns:
    -------
        ThreadOut: The thread.
    """
    category = await categories_service.get_one(id=thread_data.category)
    return await threads_service.create_thread(
        data=thread_data,
        author=user,
        category=category,
        status=ThreadStatusEnum.PENDING.value,
        thread_meta_service=thread_meta_service,
        servers_service=servers_service,
    )


@router.get("/{thread_id}")
async def get_thread(thread: Thread = Depends(get_valid_thread)) -> ThreadOut:
    """
    Get thread by id.

    Args:
    ----
        thread (Thread, optional): The thread. Defaults to Depends(get_valid_thread).

    Returns:
    -------
        ThreadOut: The thread.
    """
    return thread


@router.put("/{thread_id}", dependencies=[Depends(limiter)])
async def update_thread(
    thread_data: UpdateThreadSchema,
    thread: Thread = Depends(get_valid_thread_with_author),
) -> ThreadOut:
    """
    Update thread by id.

    Args:
    ----
        thread_data (UpdateThreadSchema): The thread data.
        thread (Thread, optional): The thread. Defaults to Depends(get_valid_thread_with_author).

    Returns:
    -------
        ThreadOut: The thread.
    """
    return await thread.update(**thread_data.dict(exclude_unset=True))
