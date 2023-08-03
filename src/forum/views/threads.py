from fastapi import Security, Depends, APIRouter, HTTPException
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Params, Page
from starlette import status

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
        kwargs["order_by"] = ["-is_pinned", queries.order_by]
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


@router.post("")
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
    # Check category type
    if category.type == CategoryTypeEnum.APPLICATION:
        # check if server_id is in thread_data
        if not thread_data.server_id:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="server_id is required")
        if not thread_data.question_experience:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="question_experience is required")
        if not thread_data.question_age:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="question_age is required")
        if not thread_data.question_reason:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="question_reason is required")

        # check if server_id is valid
        server = await servers_service.get_one(id=thread_data.server_id)

        # create new thread
        new_thread = await threads_service.create(
            title=thread_data.title,
            content=thread_data.content,
            category=category,
            author=user,
            status=ThreadStatusEnum.PENDING.value
        )

        # get thread meta by server_id
        server_id_meta_field = await thread_meta_service.get_one(name="server_id", thread_meta__id=new_thread.id)
        # update server_id_meta_field value
        await server_id_meta_field.update(value=server.id)
        # get thread meta by question_experience
        question_experience_meta_field = await thread_meta_service.get_one(name="question_experience",
                                                                           thread_meta__id=new_thread.id)
        await question_experience_meta_field.update(value=thread_data.question_experience)
        # get thread meta by question_age
        question_age_meta_field = await thread_meta_service.get_one(name="question_age", thread_meta__id=new_thread.id)
        await question_age_meta_field.update(value=thread_data.question_age)
        # get thread meta by question_reason
        question_reason_meta_field = await thread_meta_service.get_one(name="question_reason",
                                                                       thread_meta__id=new_thread.id)
        await question_reason_meta_field.update(value=thread_data.question_reason)
        return await threads_service.get_one(id=new_thread.id,
                                             related=["category", "author", "author__display_role", "meta_fields"])
    else:
        # Create normal thread
        new_thread = await threads_service.create(
            title=thread_data.title,
            content=thread_data.content,
            category=category,
            author=user
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


