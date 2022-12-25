from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.ormar import paginate

from shark_api.forum.models import Category


async def _get_categories(params: Params) -> AbstractPage:
    return await paginate(Category.objects, params)
