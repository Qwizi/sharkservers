from fastapi import APIRouter, Depends
from fastapi_pagination import Params, Page

from src.forum.dependencies import get_threads_service, get_posts_service
from src.forum.services import ThreadService, PostService
from src.roles.dependencies import get_roles_service
from src.roles.schemas import StaffRolesSchema
from src.roles.services import RoleService
from src.schemas import OrderQuery
from src.users.dependencies import get_users_service, get_valid_user
from src.users.models import User
from src.users.schemas import UserQuery, UserOut
from src.users.services import UserService

router = APIRouter()


@router.get("")
async def get_users(
        params: Params = Depends(),
        queries: UserQuery = Depends(),
        users_service: UserService = Depends(get_users_service),
) -> Page[UserOut]:
    """
    Get users
    :param users_service:
    :param params:
    :return Page[UserOut]:
    """
    kwargs = {}
    if queries.username:
        kwargs["username__contains"] = queries.username
    users = await users_service.get_all(
        params=params,
        related=["display_role", "player", "player__steamrep_profile"],
        order_by=queries.order_by,
        **kwargs
    )
    return users


@router.get("/staff")
async def get_staff_users(
        params: Params = Depends(), roles_service: RoleService = Depends(get_roles_service)
) -> Page[StaffRolesSchema]:
    """
    Get staff users
    :param users_service:
    :param params:
    :return Page[UserOut]:
    """
    return await roles_service.get_staff_roles(params)


@router.get("/online")
async def get_last_online_users(
        params: Params = Depends(), users_service: UserService = Depends(get_users_service)
) -> Page[UserOut]:
    """
    Get last logged users
    :param users_service:
    :param params:
    :return Page[UserOut]:
    """
    return await users_service.get_last_online_users(params=params)


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user: User = Depends(get_valid_user)) -> UserOut:
    """
    Get user
    :param user:
    :return UserOut:
    """
    return user


@router.get("/{user_id}/posts")
async def get_user_posts(
        params: Params = Depends(),
        queries: OrderQuery = Depends(),
        user: User = Depends(get_valid_user),
        posts_service: PostService = Depends(get_posts_service),
):
    """
    Get user posts
    :param posts_service:
    :param params:
    :param user:
    :return AbstractPage:
    """
    return await posts_service.get_all(
        params=params, author__id=user.id, order_by=queries.order_by
    )


@router.get("/{user_id}/threads")
async def get_user_threads(
        params: Params = Depends(),
        queries: OrderQuery = Depends(),
        user: User = Depends(get_valid_user),
        threads_service: ThreadService = Depends(get_threads_service),
):
    """
    Get user threads
    :param threads_service:
    :param params:
    :param user:
    :return AbstractPage:
    """
    return await threads_service.get_all(
        params=params, author__id=user.id, order_by=queries.order_by
    )
