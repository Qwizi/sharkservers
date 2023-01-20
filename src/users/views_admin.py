from fastapi import APIRouter, Depends, Security
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Page, Params, paginate
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.ormar import paginate
from ormar import NoMatch

from src.auth.schemas import RegisterUserSchema
from src.auth.dependencies import get_admin_user
from src.roles.models import Role
from src.users.enums import UsersAdminEventsEnum
from src.users.exceptions import UserNotFound
from src.users.models import User
from src.users.schemas import UserOutWithEmail, CreateUserSchema
from src.users.utils import _admin_get_users, _admin_get_user, _admin_create_user, _admin_delete_user

router = APIRouter()


@router.get("", response_model=Page[UserOutWithEmail], response_model_exclude_none=True)
async def admin_get_users(params: Params = Depends(),
                          user: User = Security(get_admin_user, scopes=["users:get_all"])) -> AbstractPage:
    """
    Admin get all users
    :param params:
    :param user:
    :return Page[UserOutWithEmail]:
    """
    dispatch(UsersAdminEventsEnum.GET_ALL_PRE, payload={"data": params})
    users = await _admin_get_users(params)
    dispatch(UsersAdminEventsEnum.GET_ALL_POST, payload={"data": users})
    return users


@router.get("/{user_id}", response_model=UserOutWithEmail)
async def admin_get_user(user_id: int,
                         user: User = Security(get_admin_user, scopes=["users:retrieve"])) -> UserOutWithEmail:
    """
    Admin get user
    :param user_id:
    :param user:
    :return UserOutWithEmail:
    """
    dispatch(UsersAdminEventsEnum.GET_ONE_PRE, payload={"data": user_id})
    user = await _admin_get_user(user_id)
    dispatch(UsersAdminEventsEnum.GET_ONE_POST, payload={"data": user})
    return user


@router.post("", response_model=UserOutWithEmail)
async def admin_create_user(user_data: CreateUserSchema,
                            user: User = Security(get_admin_user, scopes=["users:create"])) -> UserOutWithEmail:
    """
    Admin create user
    :param user_data:
    :param user:
    :return UserOutWithEmail:
    """
    dispatch(UsersAdminEventsEnum.CREATE_PRE, payload={"data": user_data})
    user = await _admin_create_user(user_data)
    dispatch(UsersAdminEventsEnum.CREATE_POST, payload={"data": user})
    return user


@router.delete("/{user_id}")
async def admin_delete_user(user_id: int, user: User = Security(get_admin_user, scopes=["users:delete"])) -> dict:
    """
    Admin delete user
    :param user_id:
    :param user:
    :return dict:
    """
    dispatch(UsersAdminEventsEnum.DELETE_PRE, payload={"data": user_id})
    user = await _admin_delete_user(user_id)
    dispatch(UsersAdminEventsEnum.DELETE_POST, payload={"data": user})
    return {"msg": "Successfully deleted user"}
