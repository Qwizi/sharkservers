"""Category views."""
from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params

from sharkservers.forum.dependencies import get_categories_service, get_valid_category
from sharkservers.forum.models import Category
from sharkservers.forum.schemas import CategoryOut
from sharkservers.forum.services import CategoryService
from sharkservers.schemas import OrderQuery

router = APIRouter()


@router.get("")
async def get_categories(
    params: Params = Depends(),
    queries: OrderQuery = Depends(),
    categories_service: CategoryService = Depends(get_categories_service),
) -> Page[CategoryOut]:
    """
    Get all categories.

    Args:
    ----
        params (Params, optional): The params. Defaults to Depends().
        queries (OrderQuery, optional): The queries. Defaults to Depends().
        categories_service (CategoryService, optional): The categories service. Defaults to Depends(get_categories_service).

    Returns:
    -------
        Page[CategoryOut]: The categories.
    """
    return await categories_service.get_all(
        params=params,
        order_by=queries.order_by,
    )


@router.get("/{category_id}")
async def get_category(category: Category = Depends(get_valid_category)) -> CategoryOut:
    """
    Get a category.

    Args:
    ----
        category (Category, optional): The category. Defaults to Depends(get_valid_category).

    Returns:
    -------
        CategoryOut: The category.
    """
    return category
