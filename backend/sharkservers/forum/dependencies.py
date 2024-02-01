"""Forum dependencies."""
from fastapi import Depends, Security
from fastapi_events.dispatcher import dispatch

from sharkservers.auth.dependencies import get_current_active_user
from sharkservers.forum.enums import PostEventEnum
from sharkservers.forum.exceptions import (
    post_not_valid_author_exception,
    thread_is_closed_exception,
    thread_not_valid_author_exception,
)
from sharkservers.forum.models import Category, Post, Thread
from sharkservers.forum.services import (
    CategoryService,
    LikeService,
    PostService,
    ThreadMetaService,
    ThreadService,
)
from sharkservers.users.models import User


async def get_categories_service() -> CategoryService:
    """Get categories service."""
    return CategoryService()


async def get_threads_service() -> ThreadService:
    """Get threads service."""
    return ThreadService()


async def get_posts_service() -> PostService:
    """Get posts service."""
    return PostService()


async def get_valid_category(
    category_id: int,
    categories_service: CategoryService = Depends(get_categories_service),
) -> Category:
    """
    Get valid category.

    Args:
    ----
        category_id (int): The category id.
        categories_service (CategoryService, optional): The categories service. Defaults to Depends(get_categories_service).

    Returns:
    -------
        Category: The category.
    """
    return await categories_service.get_one(id=category_id)


async def get_valid_thread(
    thread_id: int,
    threads_service: ThreadService = Depends(get_threads_service),
) -> Thread:
    """
    Get valid thread.

    Args:
    ----
        thread_id (int): The thread id.
        threads_service (ThreadService, optional): The threads service. Defaults to Depends(get_threads_service).

    Returns:
    -------
        Thread: The thread.
    """
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
    Get valid open thread.

    Args:
    ----
        thread (Thread, optional): The thread. Defaults to Depends(get_valid_thread).

    Returns:
    -------
        Thread: The thread.
    """
    if thread.is_closed:
        raise thread_is_closed_exception
    return thread


async def get_valid_thread_with_author(
    thread: Thread = Depends(get_valid_open_thread),
    user: User = Security(get_current_active_user, scopes=["threads:update"]),
) -> Thread:
    """
    Get valid thread with author.

    Args:
    ----
        thread (Thread, optional): The thread. Defaults to Depends(get_valid_open_thread).
        user (User, optional): The current active user. Defaults to Security(get_current_active_user, scopes=["threads:update"]).

    Returns:
    -------
        Thread: The thread.
    """
    if thread.author != user:
        raise thread_not_valid_author_exception
    return thread


async def get_valid_post(
    post_id: int,
    posts_service: PostService = Depends(get_posts_service),
) -> Post:
    """
    Get valid post.

    Args:
    ----
        post_id (int): The post id.
        posts_service (PostService, optional): The posts service. Defaults to Depends(get_posts_service).

    Returns:
    -------
        Post: The post.
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
) -> Post:
    """
    Get valid post author.

    Args:
    ----
        post (Post, optional): The post. Defaults to Depends(get_valid_post).
        user (User, optional): The current active user. Defaults to Security(get_current_active_user, scopes=["posts:update"]).

    Returns:
    -------
        Post: The post.
    """
    if post.author != user:
        raise post_not_valid_author_exception
    return post


async def get_likes_service() -> LikeService:
    """Get likes service."""
    return LikeService()


async def get_thread_meta_service() -> ThreadMetaService:
    """Get thread meta service."""
    return ThreadMetaService()
