from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.ormar import paginate

from src.forum.models import Category


async def _get_categories(params: Params) -> AbstractPage:
    return await paginate(Category.objects, params)
