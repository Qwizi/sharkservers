from fastapi import Security, Depends, APIRouter
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Params, Page

from src.auth.dependencies import get_current_active_user
from src.forum.dependencies import (
    get_valid_thread,
    get_valid_thread_with_author,
    get_threads_service,
    get_categories_service,
)
from src.forum.enums import ThreadEventEnum
from src.forum.models import Thread
from src.forum.schemas import (
    thread_out,
    CreateThreadSchema,
    ThreadOut,
    UpdateThreadSchema,
)
from src.forum.services import CategoryService, ThreadService
from src.users.models import User

router = APIRouter()


@router.get("", response_model_exclude_none=True)
async def get_threads(
    params: Params = Depends(),
    category_id: int = None,
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
    if category_id:
        threads = await threads_service.get_all(
            params=params,
            related=["category", "author", "author__display_role", "tags"],
            category__id=category_id,
        )
    else:
        threads = await threads_service.get_all(
            params=params,
            related=["category", "author", "author__display_role", "tags"],
        )
    dispatch(ThreadEventEnum.GET_ALL_POST, payload={"data": threads})
    return threads


@router.post("")
async def create_thread(
    thread_data: CreateThreadSchema,
    user: User = Security(get_current_active_user, scopes=["threads:create"]),
    threads_service: ThreadService = Depends(get_threads_service),
    categories_service: CategoryService = Depends(get_categories_service),
) -> thread_out:
    """
    Create new thread.
    :param categories_service:
    :param threads_service:
    :param thread_data:
    :param user:
    :return:
    """
    dispatch(ThreadEventEnum.CREATE_PRE, payload={"data": thread_data})
    thread_data_dict = thread_data.dict()
    category_id = thread_data_dict.pop("category")
    category = await categories_service.get_one(id=category_id)
    data = {"author": user, "category": category, **thread_data_dict}
    new_thread = await threads_service.create(**data)
    dispatch(ThreadEventEnum.CREATE_POST, payload={"data": new_thread})
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


@router.put("/{thread_id}", response_model=ThreadOut)
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
