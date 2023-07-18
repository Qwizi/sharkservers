from fastapi import APIRouter, Depends
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Page, Params

from src.forum.dependencies import get_valid_category, get_categories_service
from src.forum.enums import CategoryEventEnum
from src.forum.models import Category
from src.forum.schemas import category_out
from src.forum.services import CategoryService

router = APIRouter()


@router.get("", response_model=Page[category_out])
async def get_categories(
        params: Params = Depends(),
        categories_service: CategoryService = Depends(get_categories_service),
):
    """
    Get all categories.
    :param categories_service:
    :param params:
    :return:
    """
    dispatch(CategoryEventEnum.GET_ALL_PRE, payload={"data": params})
    categories = await categories_service.get_all(params=params)
    dispatch(CategoryEventEnum.GET_ALL_POST, payload={"data": categories})
    return categories


@router.get("/{category_id}", response_model=category_out)
async def get_category(category: Category = Depends(get_valid_category)):
    """
    Get category
    :param category:
    :return:
    """
    dispatch(CategoryEventEnum.GET_ONE_PRE, payload={"data": category.id})
    dispatch(CategoryEventEnum.GET_ONE_POST, payload={"data": category})
    return category
