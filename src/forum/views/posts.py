from fastapi import APIRouter, Depends, Security
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.ormar import paginate
from ormar import NoMatch

from src.auth.utils import get_current_active_user
from src.forum.exceptions import thread_not_found_exception, thread_is_closed_exception, post_not_found_exception
from src.forum.models import Post, Thread
from src.forum.schemas import PostOut, CreatePostSchema, UpdatePostSchema
from src.users.models import User

router = APIRouter()


@router.get("", response_model=Page[PostOut])
async def get_posts_by_thread_id(thread_id: int, params: Params = Depends()):
    posts = Post.objects.select_related(["author", "author__display_role", "thread_post"]).filter(
        thread_post__id=thread_id)
    return await paginate(posts, params)


@router.post("", response_model=PostOut)
async def create_post(post_data: CreatePostSchema,
                      user: User = Security(get_current_active_user, scopes=["posts:create"])):
    try:
        thread = await Thread.objects.get(id=post_data.thread_id)
    except NoMatch:
        raise thread_not_found_exception
    if thread.is_closed:
        raise thread_is_closed_exception
    post = await Post.objects.create(
        content=post_data.content,
        author=user
    )

    await thread.posts.add(post)
    return post


@router.put("/{post_id}")
async def update_post(post_id: int, post_data: UpdatePostSchema,
                      user: User = Security(get_current_active_user, scopes=["posts:update"])):
    try:
        post = await Post.objects.get(id=post_id)
    except NoMatch:
        raise post_not_found_exception
    if post.author.id != user.id:
        raise post_not_found_exception
    await post.update(content=post_data.content)
    return post
