from fastapi import APIRouter, Depends, Security
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Page, Params
from fastapi_pagination.bases import AbstractPage

from src.apps.dependencies import get_app_service
from src.apps.schemas import CreateAppSchema
from src.apps.services import AppService
from src.auth.dependencies import get_current_active_user, get_auth_service
from src.auth.services import AuthService
from src.forum.dependencies import get_posts_service, get_threads_service
from src.forum.services import PostService, ThreadService
from src.roles.dependencies import get_roles_service
from src.roles.schemas import StaffRolesSchema
from src.roles.services import RoleService
from src.schemas import HTTPError401Schema
from src.scopes.dependencies import get_scopes_service
from src.scopes.services import ScopeService
from src.settings import Settings, get_settings
from src.users.dependencies import get_valid_user, get_users_service
from src.users.enums import UsersEventsEnum
from src.users.models import User
from src.users.schemas import (
    UserOut,
    UserOutWithEmail,
    ChangeUsernameSchema,
    ChangePasswordSchema,
    ChangeDisplayRoleSchema,
    UserOut2Schema, SuccessChangeUsernameSchema, SuccessChangeDisplayRoleSchema,
)
from src.users.services import UserService

router = APIRouter()


@router.get("")
async def get_users(
        params: Params = Depends(), users_service: UserService = Depends(get_users_service)
) -> Page[UserOut2Schema]:
    """
    Get users
    :param users_service:
    :param params:
    :return Page[UserOut]:
    """
    dispatch(UsersEventsEnum.GET_ALL_PRE, payload={"data": params})
    users = await users_service.get_all(params=params, related=["display_role"])
    dispatch(UsersEventsEnum.GET_ALL_POST, payload={"data": users})
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


@router.get(
    "/me",
)
async def get_logged_user(
        user: User = Depends(get_current_active_user),
) -> UserOutWithEmail:
    """
    Get logged user
    :param user:
    :return UserOutWithEmail:
    """
    dispatch(UsersEventsEnum.ME_PRE, payload={"user": user})
    dispatch(UsersEventsEnum.ME_POST, payload={"user": user})
    return user


@router.get("/me/posts")
async def get_logged_user_posts(
        params: Params = Depends(),
        user: User = Security(get_current_active_user, scopes=["posts:all"]),
        posts_service: PostService = Depends(get_posts_service),
):
    """
    Get user posts
    :param params:
    :param posts_service:
    :param user:
    :return AbstractPage:
    """
    return await posts_service.get_all(params=params, author__id=user.id)


@router.get("/me/threads")
async def get_logged_user_threads(
        params: Params = Depends(),
        user: User = Security(get_current_active_user, scopes=["threads:all"]),
        threads_service: ThreadService = Depends(get_threads_service),
):
    """
    Get user threads
    :param threads_service:
    :param params:
    :param user:
    :return AbstractPage:
    """
    return await threads_service.get_all(params=params, author__id=user.id)


@router.get("/me/apps")
async def get_user_apps(
        params: Params = Depends(),
        user: User = Security(get_current_active_user, scopes=["apps:all"]),
        apps_service: AppService = Depends(get_app_service),
) -> dict:
    """
    Get user apps
    :param apps_service:
    :param user:
    :return dict:
    """
    apps = await apps_service.get_all(params=params, owner__id=user.id)
    return apps


@router.post("/me/username")
async def change_user_username(
        change_username_data: ChangeUsernameSchema,
        user: User = Security(get_current_active_user, scopes=["users:me:username"]),
        auth_service: AuthService = Depends(get_auth_service),
) -> SuccessChangeUsernameSchema:
    """
    Change user username
    :param auth_service:
    :param change_username_data:
    :param user:
    :return UserOut:
    """
    dispatch(
        UsersEventsEnum.CHANGE_USERNAME_PRE, payload={"data": change_username_data}
    )
    old_username = user.username
    user = await auth_service.change_username(user, change_username_data)
    dispatch(UsersEventsEnum.CHANGE_USERNAME_POST, payload={"data": user})
    return SuccessChangeUsernameSchema(old_username=old_username, new_username=change_username_data.username)


@router.post("/me/password")
async def change_user_password(
        change_password_data: ChangePasswordSchema,
        user: User = Security(get_current_active_user, scopes=["users:me:password"]),
        auth_service: AuthService = Depends(get_auth_service),
) -> dict:
    """
    Change user password
    :param change_password_data:
    :param user:
    :return dict:
    """
    dispatch(
        UsersEventsEnum.CHANGE_PASSWORD_PRE, payload={"data": change_password_data}
    )
    user = await auth_service.change_password(user, change_password_data)
    dispatch(UsersEventsEnum.CHANGE_PASSWORD_POST, payload={"data": user})
    return {"msg": "Successfully changed password"}


@router.post("/me/display-role")
async def change_user_display_role(
        change_display_role_data: ChangeDisplayRoleSchema,
        user: User = Security(get_current_active_user, scopes=["users:me:display-role"]),
        auth_service: AuthService = Depends(get_auth_service),
) -> SuccessChangeDisplayRoleSchema:
    """
    Change user display role
    :param auth_service:
    :param change_display_role_data:
    :param user:
    :return dict:
    """
    dispatch(
        UsersEventsEnum.CHANGE_DISPLAY_ROLE_PRE,
        payload={"data": change_display_role_data},
    )
    user, old_user_display_role = await auth_service.change_display_role(
        user, change_display_role_data
    )
    dispatch(
        UsersEventsEnum.CHANGE_DISPLAY_ROLE_POST,
        payload={"data": user, "old_user_display_role": old_user_display_role},
    )
    return SuccessChangeDisplayRoleSchema(old_display_role=old_user_display_role,
                                          new_display_role=change_display_role_data.role_id)


@router.get("/me/apps")
async def get_user_apps(
        params: Params = Depends(),
        user: User = Security(get_current_active_user, scopes=["apps:all"]),
        apps_service: AppService = Depends(get_app_service),
) -> dict:
    """
    Get user apps
    :param apps_service:
    :param user:
    :return dict:
    """
    apps = await apps_service.get_all(params=params, owner__id=user.id)
    return apps


@router.post("/me/apps")
async def create_user_app(
        app_data: CreateAppSchema,
        user: User = Security(get_current_active_user, scopes=["apps:create"]),
        apps_service: AppService = Depends(get_app_service),
        scopes_service: ScopeService = Depends(get_scopes_service),
        settings: Settings = Depends(get_settings),
) -> dict:
    """
    Create user app
    :param scopes_service:
    :param apps_service:
    :param app_data:
    :param user:
    :return dict:
    """
    app = await apps_service.create(
        name=app_data.name,
        description=app_data.description,
        owner=user,
    )
    if settings.DEBUG:
        scopes = await scopes_service.Meta.model.objects.all()
    else:
        scopes = await scopes_service.Meta.model.filter(id__in=app_data.scopes)
    for scope in scopes:
        await app.scopes.add(scope)
    return app


@router.get("/online", response_model=Page[UserOut])
async def get_last_logged_users(
        params: Params = Depends(), users_service: UserService = Depends(get_users_service)
) -> AbstractPage:
    """
    Get last logged users
    :param users_service:
    :param params:
    :return Page[UserOut]:
    """
    dispatch(UsersEventsEnum.GET_LAST_LOGGED_PRE, payload={"data": params})
    logged_users = await users_service.get_last_logged_users(params=params)
    dispatch(UsersEventsEnum.GET_LAST_LOGGED_POST, payload={"data": logged_users})
    return logged_users


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user: User = Depends(get_valid_user)) -> UserOut:
    """
    Get user
    :param user:
    :return UserOut:
    """
    dispatch(UsersEventsEnum.GET_ONE_PRE, payload={"user_id": user.id})
    dispatch(UsersEventsEnum.GET_ONE_POST, payload={"user": user})
    return user


@router.get("/{user_id}/posts")
async def get_user_posts(
        params: Params = Depends(),
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
    return await posts_service.get_all(params=params, author__id=user.id)


@router.get("/{user_id}/threads")
async def get_user_threads(
        params: Params = Depends(),
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
    return await threads_service.get_all(params=params, author__id=user.id)
