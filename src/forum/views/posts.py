from fastapi import APIRouter, Depends, Security
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.ormar import paginate
from ormar import NoMatch

from src.auth.utils import get_current_active_user
from src.forum.dependencies import get_valid_thread, get_valid_post, get_valid_post_author
from src.forum.exceptions import thread_not_found_exception, thread_is_closed_exception, post_not_found_exception
from src.forum.models import Post, Thread
from src.forum.schemas import PostOut, CreatePostSchema, UpdatePostSchema
from src.forum.services import posts_service, threads_service
from src.users.models import User

router = APIRouter()


@router.get("", response_model=Page[PostOut])
async def get_posts_by_thread_id(thread: Thread = Depends(get_valid_thread), params: Params = Depends()):
    """

    :param thread:
    :param params:
    :return:
    """
    """
    posts = Post.objects.select_related(["author", "author__display_role", "thread_post"]).filter(
        thread_post__id=thread_id)
    """
    posts = await posts_service.get_all(params=params, related=["author", "author__display_role", "thread_post"],
                                        thread_post__id=thread.id)
    return posts


@router.post("", response_model=PostOut)
async def create_post(post_data: CreatePostSchema,
                      user: User = Security(get_current_active_user, scopes=["posts:create"])):
    """

    :param post_data:
    :param user:
    :return:
    """
    post_data_dict = post_data.dict()
    thread_id = post_data_dict.pop("thread_id")
    thread: Thread = await threads_service.get_one(id=thread_id)
    if thread.is_closed:
        raise thread_is_closed_exception
    new_post = await posts_service.create(**post_data_dict, author=user)
    await thread.posts.add(new_post)
    return new_post


@router.put("/{post_id}", response_model=PostOut)
async def update_post(post_data: UpdatePostSchema, post: Post = Depends(get_valid_post_author)):
    return await post.update(**post_data.dict(exclude_unset=True))
