from fastapi import Depends, Security
from fastapi_events.dispatcher import dispatch

from src.auth.dependencies import get_current_active_user
from src.forum.enums import ThreadEventEnum, CategoryEventEnum, PostEventEnum
from src.forum.exceptions import (
    thread_is_closed_exception,
    thread_not_found_exception,
    post_not_found_exception,
)
from src.forum.models import Category, Thread, Post
from src.forum.services import categories_service, threads_service, posts_service
from src.users.models import User


async def get_valid_category(category_id: int) -> Category:
    """
    Get valid category
    :param category_id:
    :return Category:
    """
    dispatch(CategoryEventEnum.GET_ONE_PRE, payload={"data": category_id})
    return await categories_service.get_one(id=category_id)


async def get_valid_thread(thread_id: int) -> Thread:
    """
    Get valid thread
    :param thread_id:
    :return Thread:
    """
    dispatch(ThreadEventEnum.GET_ONE_PRE, payload={"data": thread_id})
    return await threads_service.get_one(
        id=thread_id, related=["category", "author", "author__display_role"]
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
        raise thread_not_found_exception
    return thread


async def get_valid_post(post_id: int) -> Post:
    """
    Get valid post
    :param post_id:
    :return Post:
    """
    dispatch(PostEventEnum.GET_ONE_PRE, payload={"data": post_id})
    return await posts_service.get_one(
        id=post_id, related=["author", "author__display_role"]
    )


async def get_valid_post_author(
    post: Post = Depends(get_valid_post),
    user: User = Security(get_current_active_user, scopes=["posts:update"]),
):
    if post.author != user:
        raise post_not_found_exception
    return post
