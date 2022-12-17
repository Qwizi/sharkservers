from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.ormar import paginate
from ormar import NoMatch

from app.forum.exceptions import TagNotFound
from app.forum.models import Tag
from app.forum.schemas import tags_out

router = APIRouter()


@router.get("", response_model=Page[tags_out])
async def get_tags(params: Params = Depends()):
    tags = Tag.objects
    return await paginate(tags, params)


@router.get("/{tag_id}", response_model=tags_out)
async def get_tag(tag_id: int):
    try:
        tag = await Tag.objects.get(id=tag_id)
        return tag
    except NoMatch:
        raise TagNotFound()
