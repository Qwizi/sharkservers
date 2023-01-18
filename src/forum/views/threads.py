from fastapi import Security, Depends, APIRouter
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.ormar import paginate
from ormar import NoMatch

from src.auth.utils import get_current_active_user
from src.forum.exceptions import thread_exists_exception, thread_not_found_exception
from src.forum.models import Thread
from src.forum.schemas import thread_out, CreateThreadSchema, ThreadOut, UpdateThreadSchema
from src.forum.utils_categories import get_category_by_id
from src.users.models import User

router = APIRouter()


@router.get("", response_model=Page[ThreadOut], response_model_exclude_none=True)
async def get_threads(category: int, params: Params = Depends()):
    threads = Thread.objects.select_related([
        "category",
        "author",
        "author__display_role",
        "tags"
    ]).filter(
        category__id=category
    )
    return await paginate(threads, params)


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


@router.get("/{thread_id}", response_model=ThreadOut)
async def get_thread(thread_id: int):
    try:

        thread = await Thread.objects.select_related(["category", "author", "author__display_role"]).get(id=thread_id)
        return thread
    except NoMatch:
        raise thread_not_found_exception


@router.put("/{thread_id}", response_model=ThreadOut)
async def update_thread(thread_id: int, thread_data: UpdateThreadSchema,
                        user: User = Security(get_current_active_user, scopes=["threads:update"])):
    try:
        thread = await Thread.objects.select_related(["category", "author", "author__display_role"]).get(id=thread_id)
        if thread.author.id != user.id:
            raise thread_not_found_exception
        await thread.update(**thread_data.dict(exclude_unset=True))
        return thread
    except NoMatch:
        raise thread_not_found_exception
