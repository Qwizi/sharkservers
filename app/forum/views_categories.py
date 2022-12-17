from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.ormar import paginate
from ormar import NoMatch

from app.forum.exceptions import CategoryNotFound
from app.forum.models import Category
from app.forum.schemas import category_out

router = APIRouter()


@router.get("", response_model=Page[category_out])
async def get_categories(params: Params = Depends()):
    categories = Category.objects
    return await paginate(categories, params)


@router.get("/{category_id}", response_model=category_out)
async def get_category(category_id: int):
    try:
        category = await Category.objects.get(id=category_id)
        return category
    except NoMatch:
        raise CategoryNotFound()
