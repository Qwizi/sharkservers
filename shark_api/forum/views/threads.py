from fastapi import Security, Depends, APIRouter
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.ormar import paginate
from ormar import NoMatch

from shark_api.auth.utils import get_current_active_user
from shark_api.forum.exceptions import thread_exists_exception, thread_not_found_exception
from shark_api.forum.models import Thread
from shark_api.forum.schemas import thread_out, CreateThread, ThreadOut
from shark_api.forum.utils_categories import get_category_by_id
from shark_api.users.models import User

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
async def create_thread(thread_data: CreateThread,
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
