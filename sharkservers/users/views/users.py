"""
Module contains the API endpoints related to users.

Endpoints:
- GET /users: Retrieves a paginated list of users based on the provided parameters.
- GET /users/staff: Retrieves a paginated list of staff users.
- GET /users/online: Retrieves a paginated list of users who were last online.
- GET /users/{user_id}: Retrieves a specific user based on the provided user ID.
- GET /users/{user_id}/posts: Retrieves a paginated list of posts made by a specific user.
- GET /users/{user_id}/threads: Retrieves a paginated list of threads created by a specific user.
"""  # noqa: E501
from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params

from sharkservers.forum.dependencies import get_posts_service, get_threads_service
from sharkservers.forum.schemas import PostOut, ThreadOut
from sharkservers.forum.services import PostService, ThreadService
from sharkservers.roles.dependencies import get_roles_service
from sharkservers.roles.schemas import StaffRolesSchema
from sharkservers.roles.services import RoleService
from sharkservers.schemas import OrderQuery
from sharkservers.users.dependencies import get_users_service, get_valid_user
from sharkservers.users.models import User
from sharkservers.users.schemas import UserOut, UserQuery
from sharkservers.users.services import UserService

router = APIRouter()


@router.get("")
async def get_users(
    params: Params = Depends(),  # noqa: B008
    queries: UserQuery = Depends(),  # noqa: B008
    users_service: UserService = Depends(get_users_service),  # noqa: B008
) -> Page[UserOut]:
    """
    Retrieve a list of users based on the provided parameters and queries.

    Args:
    ----
        params (Params, optional): The parameters for pagination and filtering. Defaults to Depends().
        queries (UserQuery, optional): The queries for filtering and ordering. Defaults to Depends().
        users_service (UserService, optional): The service for retrieving user data. Defaults to Depends(get_users_service).

    Returns:
    -------
        Page[UserOut]: The paginated list of users.

    """  # noqa: E501
    kwargs = {}
    if queries.username:
        kwargs["username__contains"] = queries.username
    return await users_service.get_all(
        params=params,
        related=["display_role", "player", "player__steamrep_profile"],
        order_by=queries.order_by,
        **kwargs,
    )


@router.get("/staff")
async def get_staff_users(
    params: Params = Depends(),  # noqa: B008
    roles_service: RoleService = Depends(get_roles_service),  # noqa: B008
) -> Page[StaffRolesSchema]:
    """
    Retrieve staff users based on the provided parameters.

    Args:
    ----
        params (Params): The parameters for filtering and pagination.
        roles_service (RoleService): The service for retrieving staff roles.

    Returns:
    -------
        Page[StaffRolesSchema]: A paginated list of staff roles.

    """
    return await roles_service.get_staff_roles(params)


@router.get("/online")
async def get_last_online_users(
    params: Params = Depends(),  # noqa: B008
    users_service: UserService = Depends(get_users_service),  # noqa: B008
) -> Page[UserOut]:
    """
    Retrieve the last online users based on the provided parameters.

    Args:
    ----
        params (Params): The parameters for filtering the users.
        users_service (UserService): The service for retrieving user data.

    Returns:
    -------
        Page[UserOut]: A paginated list of UserOut objects representing the last online users.
    """  # noqa: E501
    return await users_service.get_last_online_users(params=params)


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user: User = Depends(get_valid_user)) -> UserOut:  # noqa: B008
    """
    Retrieve the authenticated user.

    Args:
    ----
        user (User): The authenticated user.

    Returns:
    -------
        UserOut: The user object with restricted information.

    """
    return user


@router.get("/{user_id}/posts")
async def get_user_posts(
    params: Params = Depends(),  # noqa: B008
    queries: OrderQuery = Depends(),  # noqa: B008
    user: User = Depends(get_valid_user),  # noqa: B008
    posts_service: PostService = Depends(get_posts_service),  # noqa: B008
) -> Page[PostOut]:
    """
    Retrieve all posts authored by a specific user.

    Args:
    ----
        params (Params, optional): The parameters for pagination and filtering. Defaults to Depends().
        queries (OrderQuery, optional): The query parameters for ordering. Defaults to Depends().
        user (User, optional): The authenticated user. Defaults to Depends(get_valid_user).
        posts_service (PostService, optional): The service for retrieving posts. Defaults to Depends(get_posts_service).

    Returns:
    -------
        Page[PostOut]: A paginated list of PostOut objects.

    """  # noqa: E501
    return await posts_service.get_all(
        params=params,
        author__id=user.id,
        order_by=queries.order_by,
    )


@router.get("/{user_id}/threads")
async def get_user_threads(
    params: Params = Depends(),  # noqa: B008
    queries: OrderQuery = Depends(),  # noqa: B008
    user: User = Depends(get_valid_user),  # noqa: B008
    threads_service: ThreadService = Depends(get_threads_service),  # noqa: B008
) -> Page[ThreadOut]:
    """
    Retrieves all threads belonging to a specific user.

    Args:
    ----
        params (Params): The parameters for pagination and filtering.
        queries (OrderQuery): The query parameters for ordering.
        user (User): The authenticated user.
        threads_service (ThreadService): The service for managing threads.

    Returns:
    -------
        Page[ThreadOut]: A paginated list of threads belonging to the user.
    """  # noqa: D401
    return await threads_service.get_all(
        params=params,
        author__id=user.id,
        order_by=queries.order_by,
    )
