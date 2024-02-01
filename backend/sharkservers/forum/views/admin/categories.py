"""Admin categories views."""
from fastapi import APIRouter, Depends, Security

from sharkservers.auth.dependencies import get_admin_user
from sharkservers.forum.dependencies import get_categories_service, get_valid_category
from sharkservers.forum.models import Category
from sharkservers.forum.schemas import CategoryOut, CreateCategorySchema
from sharkservers.forum.services import CategoryService

router = APIRouter()


@router.post("", dependencies=[Security(get_admin_user, scopes=["categories:create"])])
async def admin_create_category(
    category_data: CreateCategorySchema,
    categories_service: CategoryService = Depends(get_categories_service),
) -> CategoryOut:
    """
    Admin create category.

    Args:
    ----
        category_data (CreateCategorySchema): The category data.
        categories_service (CategoryService, optional): The categories service. Defaults to Depends(get_categories_service).

    Returns:
    -------
        Category: The category.


    """
    return await categories_service.create(**category_data.dict())


@router.delete(
    "/{category_id}",
    dependencies=[Security(get_admin_user, scopes=["categories:delete"])],
)
async def admin_delete_category(
    category: Category = Depends(get_valid_category),
) -> CategoryOut:
    """
    Delete category.

    Args:
    ----
        category (Category, optional): The category. Defaults to Depends(get_valid_category).

    Returns:
    -------
        Category: The category.
    """
    await category.delete()
    return category
