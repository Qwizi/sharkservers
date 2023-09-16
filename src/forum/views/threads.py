from fastapi import Security, Depends, APIRouter, HTTPException
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Params, Page
from starlette import status
from fastapi_limiter.depends import RateLimiter
from src.dependencies import Limiter
from src.settings import get_settings
from src.logger import logger
from src.auth.dependencies import get_current_active_user
from src.forum.dependencies import (
    get_valid_thread,
    get_valid_thread_with_author,
    get_threads_service,
    get_categories_service, get_thread_meta_service,
)
from src.forum.enums import ThreadEventEnum, CategoryTypeEnum, ThreadStatusEnum
from src.forum.models import Thread
from src.forum.schemas import (
    ThreadOut,
    UpdateThreadSchema, CreateThreadSchema, ThreadQuery,
)
from src.forum.services import CategoryService, ThreadService, ThreadMetaService
from src.servers.dependencies import get_servers_service
from src.servers.services import ServerService
from src.users.models import User

router = APIRouter()

settings = get_settings()

limiter = RateLimiter(times=999 if settings.TESTING else 5, minutes=60 if settings.TESTING else 2)


@router.get("")
async def get_threads(
        params: Params = Depends(),
        queries: ThreadQuery = Depends(),
        threads_service: ThreadService = Depends(get_threads_service),
) -> Page[ThreadOut]:
    """
    Get all threads.
    :param threads_service:
    :param category_id:
    :param params:
    :return:
    """
    dispatch(ThreadEventEnum.GET_ALL_PRE, payload={"data": params})
    kwargs = {}
    if queries.category:
        kwargs["category__id"] = queries.category
    if queries.order_by:
        if queries.category:
            kwargs["order_by"] = ["-is_pinned", queries.order_by]
        else:
            kwargs["order_by"] = queries.order_by
    if queries.server:
        kwargs["meta_fields__name"] = "server_id"
        kwargs["meta_fields__value"] = str(queries.server)
    if queries.status:
        kwargs["status"] = queries.status
    if queries.closed:
        kwargs["is_closed"] = queries.closed

    return await threads_service.get_all(
        params=params,
        related=["category", "author", "author__display_role", "meta_fields"],
        **kwargs
    )


@router.post("", dependencies=[Depends(limiter)])
async def create_thread(
        thread_data: CreateThreadSchema,
        user: User = Security(get_current_active_user, scopes=["threads:create"]),
        threads_service: ThreadService = Depends(get_threads_service),
        categories_service: CategoryService = Depends(get_categories_service),
        thread_meta_service: ThreadMetaService = Depends(get_thread_meta_service),
        servers_service: ServerService = Depends(get_servers_service),
) -> ThreadOut:
    """
    Create new thread.
    :param thread_meta_service:
    :param categories_service:
    :param threads_service:
    :param thread_data:
    :param user:
    :return:
    """
    # Get category by id
    category = await categories_service.get_one(id=thread_data.category)
    new_thread = await threads_service.create_thread(
        data=thread_data,
        author=user,
        category=category,
        status=ThreadStatusEnum.PENDING.value,
        thread_meta_service=thread_meta_service,
        servers_service=servers_service
    )
    return new_thread


@router.get("/{thread_id}", response_model=ThreadOut)
async def get_thread(thread: Thread = Depends(get_valid_thread)):
    """
    Get thread by id.
    :param thread:
    :return:
    """
    dispatch(ThreadEventEnum.GET_ONE_POST, payload={"data": thread})
    return thread


@router.put("/{thread_id}", response_model=ThreadOut, dependencies=[Depends(limiter)])
async def update_thread(
        thread_data: UpdateThreadSchema,
        thread: Thread = Depends(get_valid_thread_with_author),
):
    """
    Update thread by id.
    :param thread_data:
    :param thread:
    :return:
    """
    dispatch(ThreadEventEnum.UPDATE_PRE, payload={"data": thread_data})
    updated_thread = await thread.update(**thread_data.dict(exclude_unset=True))
    dispatch(ThreadEventEnum.UPDATE_POST, payload={"data": updated_thread})
    return updated_thread


