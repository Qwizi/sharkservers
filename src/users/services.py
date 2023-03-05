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
    async def get_last_logged_users(params: Params) -> AbstractPage:
        filter_after = datetime.utcnow() - timedelta(minutes=15)
        return await paginate(
            User.objects.select_related("display_role").filter(
                last_login__gt=filter_after
            ),
            params,
        )


users_service = UserService(User, not_found_exception=user_not_found_exception)
