from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi_events.dispatcher import dispatch

from sharkservers.auth.dependencies import get_admin_user
from sharkservers.forum.dependencies import (
    get_categories_service,
    get_threads_service,
    get_valid_thread,
)
from sharkservers.forum.enums import ThreadActionEnum, ThreadAdminEventEnum
from sharkservers.forum.models import Thread
from sharkservers.forum.schemas import AdminThreadActionSchema, AdminUpdateThreadSchema
from sharkservers.forum.services import CategoryService, ThreadService
from sharkservers.users.dependencies import get_users_service
from sharkservers.users.models import User
from sharkservers.users.services import UserService

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
    users_service: UserService = Depends(get_users_service),
    categories_service: CategoryService = Depends(get_categories_service),
):
    update_thread_data_dict = update_thread_data.dict(exclude_unset=True)
    author_id = update_thread_data_dict.pop("author", None)
    category_id = update_thread_data_dict.pop("category", None)
    if author_id:
        author = await users_service.get_one(id=author_id)
        update_thread_data_dict["author"] = author
    if category_id:
        category = await categories_service.get_one(id=category_id)
        update_thread_data_dict["category"] = category
    update_thread = await threads_service.update(
        id=thread.id,
        updated_data=update_thread_data_dict,
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


@router.post(
    "/{thread_id}/action",
    dependencies=[Security(get_admin_user, scopes=["threads:close"])],
)
async def run_thread_action(
    data: AdminThreadActionSchema,
    thread: Thread = Depends(get_valid_thread),
    threads_service: ThreadService = Depends(get_threads_service),
    categories_service: CategoryService = Depends(get_categories_service),
):
    """
    Run thread action
    :return:
    """
    if data.action == ThreadActionEnum.MOVE:
        if not data.category:
            raise HTTPException(
                status_code=400,
                detail="Category is required for move action",
            )
        category = await categories_service.get_one(id=data.category)
        return await threads_service.run_action(
            thread=thread,
            action=data.action,
            new_category=category,
        )
    return await threads_service.run_action(thread=thread, action=data.action)
