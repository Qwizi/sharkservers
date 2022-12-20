from fastapi import APIRouter, Depends
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.ormar import paginate
from ormar import NoMatch

from app.forum.enums import CategoriesEventsEnum
from app.forum.exceptions import category_not_found_exception
from app.forum.models import Category
from app.forum.schemas import category_out
from app.forum.utils import _get_categories

router = APIRouter()


@router.get("", response_model=Page[category_out])
async def get_categories(params: Params = Depends()):
    """
    Get all categories.
    :param params:
    :return:
    """
    dispatch(CategoriesEventsEnum.GET_ALL_PRE, payload={"data": params})
    categories = await _get_categories(params)
    dispatch(CategoriesEventsEnum.GET_ALL_POST, payload={"data": categories})
    return categories


@router.get("/{category_id}", response_model=category_out)
async def get_category(category_id: int):
    try:
        category = await Category.objects.get(id=category_id)
        return category
    except NoMatch:
        raise category_not_found_exception
