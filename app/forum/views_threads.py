from fastapi import APIRouter, Depends, Security
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.ormar import paginate
from ormar import NoMatch

from app.auth.utils import get_current_active_user
from app.forum.exceptions import thread_exists_exception, category_not_found_exception, thread_not_found_exception
from app.forum.models import Thread, Category, Tag, Post
from app.forum.schemas import thread_out, CreateThread, ThreadOut
from app.users.models import User

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
    try:
        category = await Category.objects.get(id=thread_data.category)
    except NoMatch:
        raise category_not_found_exception
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
