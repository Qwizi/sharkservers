from fastapi import APIRouter, Depends, Security
from fastapi_events.dispatcher import dispatch

from src.auth.dependencies import get_admin_user
from src.forum.dependencies import (
    get_valid_thread,
    get_valid_category,
    get_threads_service,
)
from src.forum.enums import ThreadAdminEventEnum
from src.forum.models import Thread
from src.forum.schemas import AdminUpdateThreadSchema
from src.forum.services import ThreadService
from src.users.dependencies import get_valid_user
from src.users.models import User

router = APIRouter()


@router.delete("/{thread_id}")
async def admin_delete_thread(
    thread: Thread = Depends(get_valid_thread),
    user: User = Security(get_admin_user, scopes=["threads:delete"]),
    threads_service: ThreadService = Depends(get_threads_service),
):
    thread = await threads_service.delete(thread.id)
    dispatch(ThreadAdminEventEnum.DELETE_POST, payload={"data": thread.id})
    return thread


@router.put("/{thread_id}")
async def admin_update_thread(
    update_thread_data: AdminUpdateThreadSchema,
    thread: Thread = Depends(get_valid_thread),
    user: User = Security(get_admin_user, scopes=["threads:update"]),
    threads_service: ThreadService = Depends(get_threads_service),
):
    author = await get_valid_user(update_thread_data.author_id)
    category = await get_valid_category(update_thread_data.category_id)
    update_thread = await threads_service.update(
        thread__id=thread.id,
        updated_data={
            "title": update_thread_data.title,
            "content": update_thread_data.content,
            "author": author,
            "category": category,
        },
    )
    dispatch(ThreadAdminEventEnum.UPDATE_POST, payload={"data": update_thread})
    return update_thread


@router.post("/{thread_id}/close")
async def admin_close_thread(
    thread: Thread = Depends(get_valid_thread),
    user: User = Security(get_admin_user, scopes=["threads:close"]),
    threads_service: ThreadService = Depends(get_threads_service),
):
    thread = await threads_service.close_thread(thread)
    return thread


@router.post("/{thread_id}/open")
async def admin_open_thread(
    thread: Thread = Depends(get_valid_thread),
    user: User = Security(get_admin_user, scopes=["threads:open"]),
    threads_service: ThreadService = Depends(get_threads_service),
):
    thread = await threads_service.open_thread(thread)
    return thread
