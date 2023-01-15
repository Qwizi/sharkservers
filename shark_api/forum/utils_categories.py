from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.ormar import paginate
from ormar import NoMatch

from shark_api.forum.exceptions import category_not_found_exception
from shark_api.forum.models import Category


async def get_category_by_id(category_id: int) -> Category:
    try:
        return await Category.objects.get(id=category_id)
    except NoMatch:
        raise category_not_found_exception
