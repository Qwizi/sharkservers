from fastapi import APIRouter, Depends, Security
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Params
from fastapi_pagination.ext.ormar import paginate

from src.auth.dependencies import get_admin_user
from src.forum.enums import CategoriesAdminEventsEnum
from src.forum.models import Category
from src.forum.schemas import CreateCategorySchema
from src.users.models import User

router = APIRouter()


@router.get("")
async def admin_get_categories(params: Params = Depends(),
                               user: User = Security(get_admin_user, scopes=["categories:all"])):
    """
    Get all categories.
    :return:
    """
    dispatch(CategoriesAdminEventsEnum.GET_ALL_PRE, payload={"data": params})
    categories = await paginate(Category.objects, params)
    dispatch(CategoriesAdminEventsEnum.GET_ALL_POST, payload={"data": categories})
    return categories


@router.get("/{category_id}")
async def admin_get_category(category_id: int,
                             user: User = Security(get_admin_user, scopes=["categories:get"])):
    """
    Get category
    :param category_id:
    :return:
    """
    dispatch(CategoriesAdminEventsEnum.GET_ONE_PRE, payload={"data": category_id})
    category = await Category.objects.get(id=category_id)
    dispatch(CategoriesAdminEventsEnum.GET_ONE_POST, payload={"data": category})
    return category


@router.post("")
async def admin_create_category(category_data: CreateCategorySchema,
                                user: User = Security(get_admin_user, scopes=["categories:create"])):
    """
    Create category
    :param category_data:
    :return:
    """
    dispatch(CategoriesAdminEventsEnum.CREATE_PRE, payload={"data": category_data})
    category = await Category.objects.create(name=category_data.name)
    dispatch(CategoriesAdminEventsEnum.CREATE_POST, payload={"data": category})
    return category


@router.delete("/{category_id}")
async def admin_delete_category(category_id: int, user: User = Security(get_admin_user, scopes=["categories:delete"])):
    """
    Delete category
    :param category_id:
    :return:
    """
    dispatch(CategoriesAdminEventsEnum.DELETE_PRE, payload={"data": category_id})
    category = await Category.objects.get(id=category_id)
    await category.delete()
    dispatch(CategoriesAdminEventsEnum.DELETE_POST, payload={"data": category_id})
    return {"message": "Category deleted successfully."}
