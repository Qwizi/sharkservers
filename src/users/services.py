from datetime import datetime, timedelta

from asyncpg import UniqueViolationError
from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.ormar import paginate

from src.auth.schemas import RegisterUserSchema
from src.auth.utils import verify_password, get_password_hash
from src.db import BaseService
from src.roles.enums import ProtectedDefaultRolesEnum
from src.roles.services import RoleService
from src.users.exceptions import (
    username_not_available_exception,
    invalid_current_password_exception,
    cannot_change_display_role_exception,
    user_not_found_exception,
)
from src.users.models import User
from src.users.schemas import (
    ChangeUsernameSchema,
    ChangePasswordSchema,
    ChangeDisplayRoleSchema,
    CreateUserSchema,
)


class UserService(BaseService):
    @staticmethod
    async def change_username(
        user: User, change_username_data: ChangeUsernameSchema
    ) -> User:
        """
        Change user username
        :param change_username_data:
        :param user:
        :return:
        """
        try:
            await user.update(
                username=change_username_data.username, updated_date=datetime.utcnow()
            )
            return user
        except UniqueViolationError:
            raise username_not_available_exception

    @staticmethod
    async def change_password(
        user: User, change_password_data: ChangePasswordSchema
    ) -> User:
        """
        Change user password
        :param user:
        :param change_password_data:
        :return:
        """
        if not verify_password(change_password_data.current_password, user.password):
            raise invalid_current_password_exception
        new_password = get_password_hash(change_password_data.new_password)
        await user.update(password=new_password, updated_date=datetime.utcnow())
        return user

    @staticmethod
    async def change_display_role(
        user: User, change_display_role_data: ChangeDisplayRoleSchema
    ) -> (User, int):
        display_role_exists_in_user_roles = False
        old_user_display_role = user.display_role.id
        for role in user.roles:
            if role.id == change_display_role_data.role_id:
                display_role_exists_in_user_roles = True
                break
        if not display_role_exists_in_user_roles:
            raise cannot_change_display_role_exception
        await user.update(
            display_role=change_display_role_data.role_id,
            updated_date=datetime.utcnow(),
        )
        return user, old_user_display_role

    @staticmethod
    async def get_last_logged_users(params: Params) -> AbstractPage:
        filter_after = datetime.utcnow() - timedelta(minutes=15)
        return await paginate(
            User.objects.select_related("display_role").filter(
                last_login__gt=filter_after
            ),
            params,
        )


users_service = UserService(User, not_found_exception=user_not_found_exception)
