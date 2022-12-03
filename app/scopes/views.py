from fastapi import APIRouter
from fastapi_pagination import Page, paginate

from app.scopes.models import Scope

router = APIRouter()


@router.get("", response_model=Page[Scope])
async def get_all_scopes():
    scopes = await Scope.objects.all()
    return paginate(scopes)
