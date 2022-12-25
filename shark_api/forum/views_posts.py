from fastapi import APIRouter, Depends, Security
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.ormar import paginate
from ormar import NoMatch

from shark_api.auth.utils import get_current_active_user
from shark_api.forum.exceptions import thread_not_found_exception
from shark_api.forum.models import Post, Thread
from shark_api.forum.schemas import PostOut, CreatePost
from shark_api.users.models import User

router = APIRouter()


@router.get("", response_model=Page[PostOut])
async def get_posts(thread_id: int, params: Params = Depends()):
    posts = Post.objects.select_related(["author", "author__display_role", "thread_post"]).filter(
        thread_post__id=thread_id)
    return await paginate(posts, params)


@router.post("", response_model=PostOut)
async def create_post(post_data: CreatePost, user: User = Security(get_current_active_user, scopes=["posts:create"])):
    try:
        thread = await Thread.objects.get(id=post_data.thread_id)
    except NoMatch:
        raise thread_not_found_exception

    post = await Post.objects.create(
        content=post_data.content,
        author=user
    )

    await thread.posts.add(post)
    return post
