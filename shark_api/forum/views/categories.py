from fastapi import APIRouter, Depends
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.ormar import paginate
from ormar import NoMatch

from shark_api.forum.enums import CategoriesEventsEnum
from shark_api.forum.exceptions import category_not_found_exception
from shark_api.forum.models import Category
from shark_api.forum.schemas import category_out
from shark_api.forum.utils import _get_categories
from shark_api.forum.utils_categories import get_category_by_id

router = APIRouter()


@router.get("", response_model=Page[category_out])
async def get_categories(params: Params = Depends()):
    """
    Get all categories.
    :param params:
    :return:
    """
    dispatch(CategoriesEventsEnum.GET_ALL_PRE, payload={"data": params})
    categories = await paginate(Category.objects, params)
    dispatch(CategoriesEventsEnum.GET_ALL_POST, payload={"data": categories})
    return categories


@router.get("/{category_id}", response_model=category_out)
async def get_category(category_id: int):
    """
    Get category
    :param category_id:
    :return:
    """
    dispatch(CategoriesEventsEnum.GET_ONE_PRE, payload={"data": category_id})
    category = await get_category_by_id(category_id)
    dispatch(CategoriesEventsEnum.GET_ONE_POST, payload={"data": category})
    return category
