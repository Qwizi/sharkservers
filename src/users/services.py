from datetime import datetime, timedelta

from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.ormar import paginate

from src.db import BaseService
from src.forum.services import PostService
from src.users.exceptions import (
    user_not_found_exception,
)
from src.users.models import User


class UserService(BaseService):
    class Meta:
        model = User
        not_found_exception = user_not_found_exception

    async def get_last_logged_users(self, params: Params) -> AbstractPage:
        filter_after = datetime.utcnow() - timedelta(minutes=15)
        return await paginate(
            self.Meta.model.objects.select_related("display_role").filter(
                last_login__gt=filter_after
            ),
            params,
        )
