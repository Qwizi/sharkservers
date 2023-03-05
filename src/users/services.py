from datetime import datetime, timedelta

from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.ormar import paginate

from src.db import BaseService
from src.users.exceptions import (
    user_not_found_exception,
)
from src.users.models import User


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
