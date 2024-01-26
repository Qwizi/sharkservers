"""Admin posts views."""
from fastapi import APIRouter, Depends
from fastapi.params import Security

from sharkservers.auth.dependencies import get_admin_user
from sharkservers.forum.dependencies import (
    get_posts_service,
    get_threads_service,
    get_valid_post,
    get_valid_thread,
)
from sharkservers.forum.models import Post
from sharkservers.forum.schemas import (
    AdminUpdatePostSchema,
    PostOut,
)
from sharkservers.forum.services import PostService, ThreadService
from sharkservers.users.dependencies import get_users_service, get_valid_user
from sharkservers.users.services import UserService

# create router
router = APIRouter()


@router.delete(
    "/{post_id}",
    dependencies=[Security(get_admin_user, scopes=["posts:delete"])],
)
async def admin_delete_post(
    post: Post = Depends(get_valid_post),
) -> PostOut:
    """
    Admin delete post.

    Args:
    ----
        post (Post, optional): The post. Defaults to Depends(get_valid_post).

    Returns:
    -------
        Post: The post.
    """
    await post.delete()
    return post


# generate enpoint to update post via admin
@router.put(
    "/{post_id}",
    dependencies=[Security(get_admin_user, scopes=["posts:update"])],
)
async def admin_update_post(
    post_data: AdminUpdatePostSchema,
    posts_service: PostService = Depends(get_posts_service),
    threads_service: ThreadService = Depends(get_threads_service),
    users_service: UserService = Depends(get_users_service),
) -> PostOut:
    """
    Admin update post.

    Args:
    ----
        post_data (AdminUpdatePostSchema): The post data.
        posts_service (PostService, optional): The posts service. Defaults to Depends(get_posts_service).
        threads_service (ThreadService, optional): The threads service. Defaults to Depends(get_threads_service).
        users_service (UserService, optional): The users service. Defaults to Depends(get_users_service).

    Returns:
    -------
        PostOut: The post.
    """
    thread = await get_valid_thread(post_data.thread_id, threads_service)
    author = await get_valid_user(post_data.user_id, users_service)
    return await posts_service.update(
        thread__id=thread.id,
        author=author,
        content=post_data.content,
    )
