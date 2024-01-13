from fastapi import APIRouter, Depends, Security
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Page, Params

from sharkservers.auth.dependencies import get_admin_user
from sharkservers.forum.dependencies import get_categories_service, get_valid_category
from sharkservers.forum.enums import CategoryAdminEventEnum
from sharkservers.forum.models import Category
from sharkservers.forum.schemas import CategoryOut, CreateCategorySchema
from sharkservers.forum.services import CategoryService
from sharkservers.users.models import User

router = APIRouter()


@router.get(
    "",
    response_model=Page[CategoryOut],
    dependencies=[Security(get_admin_user, scopes=["categories:all"])],
)
async def admin_get_categories(
    params: Params = Depends(),
    categories_service: CategoryService = Depends(get_categories_service),
):
    """
    Get all categories.
    :param categories_service:
    :param params:
    :return:
    """
    return categories_service.get_all(params=params)


@router.get(
    "/{category_id}",
    response_model=CategoryOut,
    dependencies=[Security(get_admin_user, scopes=["categories:retrieve"])],
)
async def admin_get_category(category: Category = Depends(get_valid_category)):
    """
    Get category
    :param category:
    :return:
    """
    return category


@router.post("")
async def admin_create_category(
    category_data: CreateCategorySchema,
    user: User = Security(get_admin_user, scopes=["categories:create"]),
    categories_service: CategoryService = Depends(get_categories_service),
):
    """
    Create category
    :param categories_service:
    :param category_data:
    :return:
    """
    dispatch(CategoryAdminEventEnum.CREATE_PRE, payload={"data": category_data})
    category = await categories_service.create(**category_data.dict())
    dispatch(CategoryAdminEventEnum.CREATE_POST, payload={"data": category})
    return category


@router.delete("/{category_id}")
async def admin_delete_category(
    category: Category = Depends(get_valid_category),
    user: User = Security(get_admin_user, scopes=["categories:delete"]),
    categories_service: CategoryService = Depends(get_categories_service),
):
    """
    Delete category
    :param categories_service:
    :param user:
    :param category:
    :return:
    """
    category = await categories_service.delete(category.id)
    dispatch(CategoryAdminEventEnum.DELETE_POST, payload={"data": category})
    return {"message": "Category deleted successfully."}
