from fastapi import APIRouter, Depends, Security
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Params
from fastapi_pagination.ext.ormar import paginate

from src.auth.dependencies import get_admin_user
from src.forum.dependencies import get_valid_category
from src.forum.enums import CategoryAdminEventEnum
from src.forum.models import Category
from src.forum.schemas import CreateCategorySchema
from src.forum.services import categories_service
from src.users.models import User

router = APIRouter()


@router.post("")
async def admin_create_category(
    category_data: CreateCategorySchema,
    user: User = Security(get_admin_user, scopes=["categories:create"]),
):
    """
    Create category
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
):
    """
    Delete category
    :param user:
    :param category:
    :return:
    """
    category = await categories_service.delete(category.id)
    dispatch(CategoryAdminEventEnum.DELETE_POST, payload={"data": category})
    return {"message": "Category deleted successfully."}
