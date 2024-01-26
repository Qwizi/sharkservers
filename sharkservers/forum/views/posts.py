"""Posts views."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Security
from fastapi_events.dispatcher import dispatch
from fastapi_limiter.depends import RateLimiter
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.ormar import paginate

from sharkservers.auth.dependencies import get_current_active_user
from sharkservers.forum.dependencies import (
    get_likes_service,
    get_posts_service,
    get_threads_service,
    get_valid_post,
    get_valid_post_author,
)
from sharkservers.forum.enums import PostEventEnum
from sharkservers.forum.exceptions import (
    thread_is_closed_exception,
)
from sharkservers.forum.models import Post
from sharkservers.forum.schemas import (
    CreatePostSchema,
    LikeOut,
    PostOut,
    PostQuery,
    UpdatePostSchema,
)
from sharkservers.forum.services import LikeService, PostService, ThreadService
from sharkservers.settings import get_settings
from sharkservers.users.models import User

router = APIRouter()

settings = get_settings()
limiter = RateLimiter(
    times=999 if settings.TESTING else 5,
    minutes=60 if settings.TESTING else 1,
)


@router.get("")
async def get_posts(
    thread_id: int | None = None,
    params: Params = Depends(),
    queries: PostQuery = Depends(),
    posts_service: PostService = Depends(get_posts_service),
) -> Page[PostOut]:
    """
    Get all posts.

    Args:
    ----
        thread_id (int, optional): The thread ID. Defaults to None.
        params (Params, optional): The params. Defaults to Depends().
        queries (PostQuery, optional): The queries. Defaults to Depends().
        posts_service (PostService, optional): The posts service. Defaults to Depends(get_posts_service).

    Returns:
    -------
        Page[PostOut]: The posts.
    """
    kwargs = {}
    if thread_id:
        kwargs["thread_post__id"] = thread_id
    return await posts_service.get_all(
        params=params,
        related=[
            "author",
            "author__display_role",
            "thread_post",
            "author__player",
            "author__player__steamrep_profile",
        ],
        order_by=queries.order_by,
        **kwargs,
    )


@router.get("/{post_id}")
async def get_post_by_id(post: Post = Depends(get_valid_post)) -> PostOut:
    """
    Get post by ID.

    Args:
    ----
        post (Post): The post. Defaults to Depends(get_valid_post).

    Returns:
    -------
        Post: The post.
    """
    return post


@router.post("", dependencies=[Depends(limiter)])
async def create_post(
    post_data: CreatePostSchema,
    user: User = Security(get_current_active_user, scopes=["posts:create"]),
    posts_service: PostService = Depends(get_posts_service),
    threads_service: ThreadService = Depends(get_threads_service),
) -> PostOut:
    """
    Create post.

    Args:
    ----
        post_data (CreatePostSchema): The post data.
        user (User, optional): The user. Defaults to Security(get_current_active_user, scopes=["posts:create"]).
        posts_service (PostService, optional): The posts service. Defaults to Depends(get_posts_service).
        threads_service (ThreadService, optional): The threads service. Defaults to Depends(get_threads_service).

    Raises:
    ------
        thread_is_closed_exception: The thread is closed exception.

    Returns:
    -------
        PostOut: The post.
    """
    post_data_dict = post_data.dict()
    thread_id = post_data_dict.pop("thread_id")
    thread = await threads_service.get_one(id=thread_id)
    if thread.is_closed:
        raise thread_is_closed_exception
    new_post = await posts_service.create(**post_data_dict, author=user)
    await thread.posts.add(new_post)
    dispatch(PostEventEnum.CREATE_POST, payload={"data": new_post})
    return new_post


@router.put("/{post_id}", dependencies=[Depends(limiter)])
async def update_post(
    post_data: UpdatePostSchema,
    post: Post = Depends(get_valid_post_author),
) -> PostOut:
    """
    Update post.

    Args:
    ----
        post_data (UpdatePostSchema): The post data.
        post (Post, optional): The post. Defaults to Depends(get_valid_post_author).

    Returns:
    -------
        Post: The post.
    """
    return await post.update(**post_data.dict(exclude_unset=True))


@router.get("/{post_id}/likes")
async def get_post_likes(
    post: Post = Depends(get_valid_post),
    likes_service: LikeService = Depends(get_likes_service),
    params: Params = Depends(),
) -> Page[LikeOut]:
    """
    Get post likes.

    Args:
    ----
        post (Post, optional): The post. Defaults to Depends(get_valid_post).
        likes_service (LikeService, optional): The likes service. Defaults to Depends(get_likes_service).
        params (Params, optional): The params. Defaults to Depends().

    Returns:
    -------
        Page[LikeOut]: The likes.
    """
    return await paginate(
        likes_service.Meta.model.objects.select_related(
            ["author", "post_likes", "author__display_role"],
        ).filter(post_likes__id=post.id),
        params,
    )


@router.post("/{post_id}/like", dependencies=[Depends(limiter)])
async def like_post(
    post: Post = Depends(get_valid_post),
    user: User = Security(get_current_active_user, scopes=["posts:create"]),
    likes_service: LikeService = Depends(get_likes_service),
) -> LikeOut:
    """
    Like post.

    Args:
    ----
        post (Post, optional): The post. Defaults to Depends(get_valid_post).
        user (User, optional): The user. Defaults to Security(get_current_active_user, scopes=["posts:create"]).
        likes_service (LikeService, optional): The likes service. Defaults to Depends(get_likes_service).

    Returns:
    -------
        LikeOut: The like.
    """
    new_like, likes = await likes_service.add_like_to_post(post=post, author=user)
    return new_like


@router.post("/{post_id}/dislike", dependencies=[Depends(limiter)])
async def dislike_post(
    post: Post = Depends(get_valid_post),
    user: User = Security(get_current_active_user, scopes=["posts:create"]),
    likes_service: LikeService = Depends(get_likes_service),
) -> dict:
    """
    Dislike post.

    Args:
    ----
        post (Post, optional): The post. Defaults to Depends(get_valid_post).
        user (User, optional): The user. Defaults to Security(get_current_active_user, scopes=["posts:create"]).
        likes_service (LikeService, optional): The likes service. Defaults to Depends(get_likes_service).

    Returns:
    -------
        dict: The response.
    """
    return await likes_service.remove_like_from_post(post=post, author=user)
