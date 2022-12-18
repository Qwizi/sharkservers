from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.ormar import paginate

from app.users.models import User


async def _get_users(params: Params) -> AbstractPage:
    """
    Get users
    :param params:
    :return:
    """
    return await paginate(User.objects.select_related(["display_role"]), params)
