from fastapi import APIRouter, Depends
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Page, Params
from sharkservers.forum.dependencies import get_categories_service, get_valid_category
from sharkservers.forum.enums import CategoryEventEnum
from sharkservers.forum.models import Category
from sharkservers.forum.schemas import CategoryOut
from sharkservers.forum.services import CategoryService
from sharkservers.schemas import OrderQuery

router = APIRouter()


@router.get("", response_model=Page[CategoryOut])
async def get_categories(
    params: Params = Depends(),
    queries: OrderQuery = Depends(),
    categories_service: CategoryService = Depends(get_categories_service),
):
    """
    Get all categories.
    :param categories_service:
    :param params:
    :return:
    """
    dispatch(CategoryEventEnum.GET_ALL_PRE, payload={"data": params})
    categories = await categories_service.get_all(
        params=params,
        order_by=queries.order_by,
    )
    dispatch(CategoryEventEnum.GET_ALL_POST, payload={"data": categories})
    return categories


@router.get("/{category_id}", response_model=CategoryOut)
async def get_category(category: Category = Depends(get_valid_category)):
    """
    Get category
    :param category:
    :return:
    """
    dispatch(CategoryEventEnum.GET_ONE_PRE, payload={"data": category.id})
    dispatch(CategoryEventEnum.GET_ONE_POST, payload={"data": category})
    return category
