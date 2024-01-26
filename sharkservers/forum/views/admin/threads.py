"""Admin threads views."""
from fastapi import APIRouter, Depends, HTTPException, Security

from sharkservers.auth.dependencies import get_admin_user
from sharkservers.forum.dependencies import (
    get_categories_service,
    get_threads_service,
    get_valid_category,
    get_valid_thread,
)
from sharkservers.forum.enums import ThreadActionEnum
from sharkservers.forum.models import Thread
from sharkservers.forum.schemas import (
    AdminThreadActionSchema,
    AdminUpdateThreadSchema,
    ThreadOut,
)
from sharkservers.forum.services import CategoryService, ThreadService
from sharkservers.users.dependencies import get_users_service, get_valid_user
from sharkservers.users.services import UserService

router = APIRouter()

"""  """


@router.delete(
    "/{thread_id}",
    dependencies=[Security(get_admin_user, scopes=["threads:delete"])],
)
async def admin_delete_thread(
    thread: Thread = Depends(get_valid_thread),
) -> ThreadOut:
    """
    Delete thread.

    Args:
    ----
        thread (Thread, optional): The thread. Defaults to Depends(get_valid_thread).

    Returns:
    -------
        Thread: The thread.
    """
    await thread.delete()
    return thread


@router.put(
    "/{thread_id}",
    dependencies=[Security(get_admin_user, scopes=["threads:update"])],
)
async def admin_update_thread(
    update_thread_data: AdminUpdateThreadSchema,
    thread: Thread = Depends(get_valid_thread),
    threads_service: ThreadService = Depends(get_threads_service),
    users_service: UserService = Depends(get_users_service),
    categories_service: CategoryService = Depends(get_categories_service),
) -> ThreadOut:
    """
    Update thread.

    Args:
    ----
        update_thread_data (AdminUpdateThreadSchema): The update thread data.
        thread (Thread, optional): The thread. Defaults to Depends(get_valid_thread).
        threads_service (ThreadService, optional): The threads service. Defaults to Depends(get_threads_service).
        users_service (UserService, optional): The users service. Defaults to Depends(get_users_service).
        categories_service (CategoryService, optional): The categories service. Defaults to Depends(get_categories_service).

    Returns:
    -------
        Thread: The thread.
    """
    update_thread_data_dict = update_thread_data.dict(exclude_unset=True)
    author_id = update_thread_data_dict.pop("author", None)
    category_id = update_thread_data_dict.pop("category", None)
    if author_id:
        author = await get_valid_user(author_id, users_service=users_service)
        update_thread_data_dict["author"] = author
    if category_id:
        category = await get_valid_category(
            category_id,
            categories_service=categories_service,
        )
        update_thread_data_dict["category"] = category
    return await threads_service.update(
        id=thread.id,
        updated_data=update_thread_data_dict,
    )


@router.post(
    "/{thread_id}/action",
    dependencies=[Security(get_admin_user, scopes=["threads:close"])],
)
async def run_thread_action(
    data: AdminThreadActionSchema,
    thread: Thread = Depends(get_valid_thread),
    categories_service: CategoryService = Depends(get_categories_service),
) -> ThreadOut:
    """
    Run thread action.

    Args:
    ----
        data (AdminThreadActionSchema): The data.
        thread (Thread, optional): The thread. Defaults to Depends(get_valid_thread).
        threads_service (ThreadService, optional): The threads service. Defaults to Depends(get_threads_service).
        categories_service (CategoryService, optional): The categories service. Defaults to Depends(get_categories_service).

    Raises:
    ------
        HTTPException: The HTTP exception.

    Returns:
    -------
        ThreadOut: The thread.

    """
    if data.action == ThreadActionEnum.MOVE:
        if not data.category:
            raise HTTPException(
                status_code=400,
                detail="Category is required for move action",
            )
        category = await get_valid_category(
            data.category,
            categories_service=categories_service,
        )
        await thread.run_action(
            action=data.action,
            new_category=category,
        )
    await thread.run_action(action=data.action)
    return thread
