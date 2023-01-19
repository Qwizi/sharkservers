from typing import Optional

from fastapi import Security, Depends, APIRouter
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.ormar import paginate
from ormar import NoMatch

from src.auth.utils import get_current_active_user
from src.forum.dependencies import get_valid_category, get_valid_thread, get_valid_thread_with_author, \
    get_valid_open_thread
from src.forum.exceptions import thread_exists_exception, thread_not_found_exception
from src.forum.models import Thread, Category
from src.forum.schemas import thread_out, CreateThreadSchema, ThreadOut, UpdateThreadSchema, CreatePostSchema
from src.forum.services import threads_service, categories_service, posts_service
from src.forum.utils_categories import get_category_by_id
from src.users.models import User

router = APIRouter()


@router.get("", response_model=Page[ThreadOut], response_model_exclude_none=True)
async def get_threads(params: Params = Depends()):
    return await threads_service.get_all(params=params, related=["category",
                                                                 "author",
                                                                 "author__display_role",
                                                                 "tags"])


"""
@router.post("", response_model=thread_out)
async def create_thread(thread_data: CreateThreadSchema,
                        user: User = Security(get_current_active_user, scopes=["threads:create"])):
    category = await get_category_by_id(thread_data.category)
    thread_exists = await Thread.objects.select_related(["category"]).filter(title=thread_data.title,
                                                                             category__id=category).exists()
    if thread_exists:
        raise thread_exists_exception
    thread = await Thread.objects.create(
        title=thread_data.title,
        content=thread_data.content,
        category=category,
        author=user
    )
    return thread
"""


@router.post("", response_model=thread_out)
async def create_thread(thread_data: CreateThreadSchema,
                        user: User = Security(get_current_active_user, scopes=["threads:create"])):
    thread_data_dict = thread_data.dict()
    category_id = thread_data_dict.pop("category")
    category = await categories_service.get_one(id=category_id)
    data = {"author": user, "category": category, **thread_data_dict}
    new_thread = await threads_service.create(**data)
    return new_thread


@router.get("/{thread_id}", response_model=ThreadOut)
async def get_thread(thread: Thread = Depends(get_valid_thread)):
    return thread


@router.put("/{thread_id}", response_model=ThreadOut)
async def update_thread(thread_data: UpdateThreadSchema, thread: Thread = Depends(get_valid_thread_with_author)):
    updated_thread = await threads_service.update(id=thread.id, updated_data=thread_data.dict(exclude_unset=True),
                                                  related=["category", "author", "author__display_role"])
    return updated_thread
