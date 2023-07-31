from datetime import datetime, timedelta

from fastapi_pagination import Params, Page
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.ormar import paginate

from src.auth.utils import now_datetime
from src.db import BaseService
from src.forum.services import PostService
from src.users.exceptions import (
    user_not_found_exception,
)
from src.users.models import User
from src.users.schemas import UserOut


class UserService(BaseService):
    class Meta:
        model = User
        not_found_exception = user_not_found_exception

    async def get_last_online_users(self, params: Params) -> Page[UserOut]:
        filter_after = now_datetime() - timedelta(minutes=15)
        return await self.get_all(params=params, related=["display_role"], last_online__gt=filter_after)
