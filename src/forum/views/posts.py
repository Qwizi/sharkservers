from fastapi import APIRouter, Depends, Security
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.ormar import paginate

from src.auth.dependencies import get_current_active_user
from src.forum.dependencies import (
    get_valid_post,
    get_valid_post_author,
    get_posts_service,
    get_threads_service, get_likes_service,
)
from src.forum.enums import PostEventEnum
from src.forum.exceptions import (
    thread_is_closed_exception,
)
from src.forum.models import Post
from src.forum.schemas import PostOut, CreatePostSchema, UpdatePostSchema, LikeOut
from src.forum.services import PostService, ThreadService, LikeService
from src.users.models import User

router = APIRouter()


@router.get("")
async def get_posts(
        thread_id: int = None,
        params: Params = Depends(),
        posts_service: PostService = Depends(get_posts_service),
) -> Page[PostOut]:
    """
    Get all posts by thread id.
    :param posts_service:
    :param thread_id:
    :param params:
    :return:
    """
    kwargs = {}
    if thread_id:
        kwargs["thread_post__id"] = thread_id
    return await posts_service.get_all(
            params=params,
            related = ["author", "author__display_role", "thread_post"],
            order_by="id",
            **kwargs
        )


@router.get("/{post_id}", response_model=PostOut)
async def get_post_by_id(post: Post = Depends(get_valid_post)):
    """
    Get post by id.
    :param post:
    :return:
    """
    return post


@router.post("")
async def create_post(
        post_data: CreatePostSchema,
        user: User = Security(get_current_active_user, scopes=["posts:create"]),
        posts_service: PostService = Depends(get_posts_service),
        threads_service: ThreadService = Depends(get_threads_service),
) -> PostOut:
    """

    :param threads_service:
    :param posts_service:
    :param post_data:
    :param user:
    :return:
    """
    dispatch(PostEventEnum.CREATE_PRE, payload={"data": post_data})
    post_data_dict = post_data.dict()
    thread_id = post_data_dict.pop("thread_id")
    thread = await threads_service.get_one(id=thread_id)
    if thread.is_closed:
        raise thread_is_closed_exception
    new_post = await posts_service.create(**post_data_dict, author=user)
    await thread.posts.add(new_post)
    dispatch(PostEventEnum.CREATE_POST, payload={"data": new_post})
    return new_post


@router.put("/{post_id}", response_model=PostOut)
async def update_post(
        post_data: UpdatePostSchema, post: Post = Depends(get_valid_post_author)
):
    post_updated = await post.update(**post_data.dict(exclude_unset=True))
    dispatch(PostEventEnum.UPDATE_POST, payload={"data": post_updated})
    return post_updated


@router.get("/{post_id}/likes")
async def get_post_likes(
        post: Post = Depends(get_valid_post),
        likes_service: LikeService = Depends(get_likes_service),
        params: Params = Depends(),
) -> Page[LikeOut]:
    """
    Get all post likes.
    :param post:
    :param likes_service:
    :return:
    """
    return await paginate(
        likes_service.Meta.model.objects.select_related(["author", "post_likes", "author__display_role"]).filter(post_likes__id=post.id),
        params)


@router.post("/{post_id}/like")
async def like_post(
        post: Post = Depends(get_valid_post),
        user: User = Security(get_current_active_user, scopes=["posts:create"]),
        likes_service: LikeService = Depends(get_likes_service),
):
    """
    Like post.
    :param post:
    :param user:
    :param likes_service:
    :return:
    """
    new_like, likes = await likes_service.add_like_to_post(post=post, author=user)
    return {"message": "Post liked successfully", "data": {"new_like": new_like, "likes": likes}}


@router.post("/{post_id}/dislike")
async def dislike_post(
        post: Post = Depends(get_valid_post),
        user: User = Security(get_current_active_user, scopes=["posts:create"]),
        likes_service: LikeService = Depends(get_likes_service),
):
    """
    Dislike post.
    :param post:
    :param user:
    :param likes_service:
    :return:
    """
    return await likes_service.remove_like_from_post(post=post, author=user)
