from fastapi import Depends, Security
from fastapi_events.dispatcher import dispatch
from ormar import Model

from sharkservers.auth.dependencies import get_current_active_user
from sharkservers.forum.enums import CategoryEventEnum, PostEventEnum, ThreadEventEnum
from sharkservers.forum.exceptions import (
    post_not_valid_author_exception,
    thread_is_closed_exception,
    thread_not_valid_author_exception,
)
from sharkservers.forum.models import Post, Thread
from sharkservers.forum.services import (
    CategoryService,
    LikeService,
    PostService,
    ThreadMetaService,
    ThreadService,
)
from sharkservers.users.models import User


async def get_categories_service() -> CategoryService:
    return CategoryService()


async def get_threads_service() -> ThreadService:
    return ThreadService()


async def get_posts_service() -> PostService:
    return PostService()


async def get_valid_category(
    category_id: int,
    categories_service: CategoryService = Depends(get_categories_service),
) -> Model:
    """
    Get valid category
    :param categories_service:
    :param category_id:
    :return Category:
    """
    dispatch(CategoryEventEnum.GET_ONE_PRE, payload={"data": category_id})
    return await categories_service.get_one(id=category_id)


async def get_valid_thread(
    thread_id: int,
    threads_service: ThreadService = Depends(get_threads_service),
) -> Model:
    """
    Get valid thread
    :param threads_service:
    :param thread_id:
    :return Thread:
    """
    dispatch(ThreadEventEnum.GET_ONE_PRE, payload={"data": thread_id})
    return await threads_service.get_one(
        id=thread_id,
        related=[
            "category",
            "author",
            "author__display_role",
            "author__player",
            "author__player__steamrep_profile",
            "meta_fields",
            "server",
            "server__admin_role",
        ],
    )


async def get_valid_open_thread(thread: Thread = Depends(get_valid_thread)) -> Thread:
    """
    Get valid open thread
    :param thread:
    :param thread_id:
    :return Thread:
    """
    if thread.is_closed:
        raise thread_is_closed_exception
    return thread


async def get_valid_thread_with_author(
    thread: Thread = Depends(get_valid_open_thread),
    user: User = Security(get_current_active_user, scopes=["threads:update"]),
):
    """
    Get valid thread with author
    :param thread:
    :param user:
    :return Thread:
    """
    if thread.author != user:
        raise thread_not_valid_author_exception
    return thread


async def get_valid_post(
    post_id: int,
    posts_service: PostService = Depends(get_posts_service),
):
    """
    Get valid post
    :param posts_service:
    :param post_id:
    :return Post:
    """
    dispatch(PostEventEnum.GET_ONE_PRE, payload={"data": post_id})
    return await posts_service.get_one(
        id=post_id,
        related=[
            "author",
            "author__display_role",
            "likes",
            "author__player",
            "author__player__steamrep_profile",
        ],
    )


async def get_valid_post_author(
    post: Post = Depends(get_valid_post),
    user: User = Security(get_current_active_user, scopes=["posts:update"]),
):
    if post.author != user:
        raise post_not_valid_author_exception
    return post


async def get_likes_service() -> LikeService:
    return LikeService()


async def get_thread_meta_service() -> ThreadMetaService:
    return ThreadMetaService()
