from datetime import datetime, timedelta

from asyncpg import UniqueViolationError
from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.ormar import paginate
from ormar import NoMatch

from app.auth.utils import verify_password, get_password_hash
from app.users.exceptions import username_not_available_exception, invalid_current_password_exception, \
    cannot_change_display_role_exception, user_not_found_exception
from app.users.models import User
from app.users.schemas import ChangeUsernameSchema, ChangePasswordSchema, ChangeDisplayRoleSchema


async def _get_users(params: Params) -> AbstractPage:
    """
    Get users
    :param params:
    :return:
    """
    return await paginate(User.objects.select_related(["display_role"]), params)


async def _change_user_username(change_username_data: ChangeUsernameSchema, user: User) -> User:
    """
    Change user username
    :param change_username_data:
    :param user:
    :return:
    """
    try:
        await user.update(username=change_username_data.username, updated_date=datetime.utcnow())
        return user
    except UniqueViolationError:
        raise username_not_available_exception


async def _change_user_password(change_password_data: ChangePasswordSchema, user: User) -> User:
    if not verify_password(change_password_data.current_password, user.password):
        raise invalid_current_password_exception
    new_password = get_password_hash(change_password_data.new_password)
    await user.update(password=new_password, updated_date=datetime.utcnow())
    return user


async def _change_user_display_role(change_display_role_data: ChangeDisplayRoleSchema, user: User) -> (User, int):
    """
    Change user display role
    :param change_display_role_data:
    :param user:
    :return:
    """
    display_role_exists_in_user_roles = False
    old_user_display_role = user.display_role.id
    for role in user.roles:
        if role.id == change_display_role_data.role_id:
            display_role_exists_in_user_roles = True
            break
    if not display_role_exists_in_user_roles:
        raise cannot_change_display_role_exception
    await user.update(display_role=change_display_role_data.role_id, updated_date=datetime.utcnow())
    return user, old_user_display_role


async def _get_last_logged_users(params: Params) -> AbstractPage:
    filter_after = datetime.utcnow() - timedelta(minutes=15)
    return await paginate(User.objects.select_related("display_role").filter(
        last_login__gt=filter_after), params)


async def _get_user(user_id: int) -> User:
    try:
        return await User.objects.select_related(["roles", "display_role"]).get(id=user_id)
    except NoMatch:
        raise user_not_found_exception
