# Path forum/views/threads.py
from fastapi import APIRouter, Depends
from fastapi.params import Security
from fastapi_events.dispatcher import dispatch

from src.auth.dependencies import get_admin_user
from src.forum.dependencies import get_valid_thread, get_valid_post
from src.forum.enums import PostAdminEventEnum
from src.forum.models import Thread, Post
from src.forum.schemas import AdminCreatePostSchema, AdminUpdatePostSchema
from src.forum.services import posts_service
from src.users.dependencies import get_valid_user
from src.users.models import User

# create router
router = APIRouter()


# generate enpoint to create post via admin
@router.post("/")
async def admin_create_post(
    post_data: AdminCreatePostSchema,
    user: User = Security(get_admin_user, scopes=["posts:create"]),
):
    """
    Create post
    :param post_data:
    :param thread:
    :param user:
    :return:
    """
    dispatch(PostAdminEventEnum.CREATE_PRE, payload={"data": post_data})
    thread = await get_valid_thread(post_data.thread_id)
    author = await get_valid_user(post_data.user_id)
    new_post = await posts_service.create(
        thread__id=thread.id, author=author, content=post_data.content
    )
    dispatch(PostAdminEventEnum.CREATE_POST, payload={"data": new_post})
    return new_post


# generate enpoint to delete post via admin
@router.delete("/{post_id}")
async def admin_delete_post(
    post: Post = Depends(get_valid_post),
    user: User = Security(get_admin_user, scopes=["posts:delete"]),
):
    """
    Delete post
    :param post:
    :param user:
    :param post_id:
    :return:
    """
    post = await posts_service.delete(post.id)
    dispatch(PostAdminEventEnum.DELETE_POST, payload={"data": post})
    return post


# generate enpoint to update post via admin
@router.put("/{post_id}")
async def admin_update_post(
    post_data: AdminUpdatePostSchema,
    post: Post = Depends(get_valid_post),
    user: User = Security(get_admin_user, scopes=["posts:update"]),
):
    """
    Update post
    :param post:
    :param post_data:
    :param user:
    :return:
    """
    dispatch(PostAdminEventEnum.UPDATE_PRE, payload={"data": post_data})
    thread = await get_valid_thread(post_data.thread_id)
    author = await get_valid_user(post_data.user_id)
    post = await posts_service.update(
        thread__id=thread.id,
        author=author,
        content=post_data.content,
    )
    dispatch(PostAdminEventEnum.UPDATE_POST, payload={"data": post})
    return post
