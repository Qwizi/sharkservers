from fastapi import APIRouter, Depends, Security
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Page, Params
from fastapi_pagination.bases import AbstractPage

from src.auth.schemas import RegisterUserSchema
from src.auth.dependencies import get_current_active_user
from src.schemas import HTTPError401Schema
from src.users.dependencies import get_valid_user
from src.users.enums import UsersEventsEnum
from src.users.models import User
from src.users.schemas import (
    UserOut,
    UserOutWithEmail,
    ChangeUsernameSchema,
    ChangePasswordSchema,
    ChangeDisplayRoleSchema,
    UserOut2Schema,
    CreateUserSchema,
)
from src.users.services import users_service
from src.users.utils import (
    _get_users,
    _change_user_username,
    _change_user_password,
    _change_user_display_role,
    _get_last_logged_users,
    _get_user,
)

router = APIRouter()


@router.get("", response_model=Page[UserOut2Schema])
async def get_users(params: Params = Depends()) -> AbstractPage:
    """
    Get users
    :param params:
    :return Page[UserOut]:
    """
    dispatch(UsersEventsEnum.GET_ALL_PRE, payload={"data": params})
    users = await users_service.get_all(params=params, related=["display_role"])
    dispatch(UsersEventsEnum.GET_ALL_POST, payload={"data": users})
    return users


@router.get(
    "/me",
    response_model=UserOutWithEmail,
    responses={401: {"model": HTTPError401Schema}},
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


@router.post("/me/username", response_model=UserOut)
async def change_user_username(
    change_username_data: ChangeUsernameSchema,
    user: User = Security(get_current_active_user, scopes=["users:me:username"]),
) -> UserOut:
    """
    Change user username
    :param change_username_data:
    :param user:
    :return UserOut:
    """
    dispatch(
        UsersEventsEnum.CHANGE_USERNAME_PRE, payload={"data": change_username_data}
    )
    user = await users_service.change_username(user, change_username_data)
    dispatch(UsersEventsEnum.CHANGE_USERNAME_POST, payload={"data": user})
    return user


@router.post("/me/password")
async def change_user_password(
    change_password_data: ChangePasswordSchema,
    user: User = Security(get_current_active_user, scopes=["users:me:password"]),
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
    user = await users_service.change_password(user, change_password_data)
    dispatch(UsersEventsEnum.CHANGE_PASSWORD_POST, payload={"data": user})
    return {"msg": "Successfully changed password"}


@router.post("/me/display-role")
async def change_user_display_role(
    change_display_role_data: ChangeDisplayRoleSchema,
    user: User = Security(get_current_active_user, scopes=["users:me:display-role"]),
) -> dict:
    """
    Change user display role
    :param change_display_role_data:
    :param user:
    :return dict:
    """
    dispatch(
        UsersEventsEnum.CHANGE_DISPLAY_ROLE_PRE,
        payload={"data": change_display_role_data},
    )
    user, old_user_display_role = await users_service.change_display_role(
        user, change_display_role_data
    )
    dispatch(
        UsersEventsEnum.CHANGE_DISPLAY_ROLE_POST,
        payload={"data": user, "old_user_display_role": old_user_display_role},
    )
    return {
        "old_display_role": old_user_display_role,
        "new_display_role": change_display_role_data.role_id,
    }


@router.get("/online", response_model=Page[UserOut])
async def get_last_logged_users(params: Params = Depends()) -> AbstractPage:
    """
    Get last logged users
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
    :param user_id:
    :return UserOut:
    """
    dispatch(UsersEventsEnum.GET_ONE_PRE, payload={"user_id": user.id})
    dispatch(UsersEventsEnum.GET_ONE_POST, payload={"user": user})
    return user
