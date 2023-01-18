from fastapi import APIRouter, Depends, Security
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.ormar import paginate
from ormar import NoMatch

from src.auth.utils import get_admin_user
from src.forum.exceptions import thread_not_found_exception
from src.forum.models import Thread
from src.forum.schemas import ThreadOut, UpdateThreadSchema
from src.users.models import User

router = APIRouter()


@router.get("", response_model=Page[ThreadOut], response_model_exclude_none=True)
async def admin_get_threads(params: Params = Depends(),
                            user: User = Security(get_admin_user, scopes=["threads:get_all"])):
    threads = Thread.objects.select_related([
        "category",
        "author",
        "author__display_role",
        "tags"
    ])
    return await paginate(threads, params)


@router.delete("/{thread_id}")
async def admin_delete_thread(thread_id: int, user: User = Security(get_admin_user, scopes=["threads:delete"])):
    try:
        thread = await Thread.objects.get(id=thread_id)
        await thread.delete()
    except NoMatch:
        raise thread_not_found_exception
    return {"message": "Thread deleted successfully"}


@router.put("/{thread_id}")
async def admin_update_thread(thread_id: int, update_thread_data: UpdateThreadSchema,
                              user: User = Security(get_admin_user, scopes=["threads:update"])):
    try:
        thread = await Thread.objects.get(id=thread_id)
        await thread.update(**update_thread_data.dict(exclude_unset=True))
    except NoMatch:
        raise thread_not_found_exception
    return thread


@router.post("/{thread_id}/close")
async def admin_close_thread(thread_id: int, user: User = Security(get_admin_user, scopes=["threads:close"])):
    try:
        thread = await Thread.objects.get(id=thread_id)
        await thread.update(is_closed=True)
    except NoMatch:
        raise thread_not_found_exception
    return thread


@router.post("/{thread_id}/open")
async def admin_open_thread(thread_id: int, user: User = Security(get_admin_user, scopes=["threads:open"])):
    try:
        thread = await Thread.objects.get(id=thread_id)
        await thread.update(is_closed=False)
    except NoMatch:
        raise thread_not_found_exception
    return thread
