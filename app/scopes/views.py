from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.ormar import paginate

from app.scopes.exceptions import RoleScopeNotFound
from app.scopes.models import Scope
from app.scopes.schemas import ScopeOut

router = APIRouter()


@router.get("", response_model=Page[ScopeOut], response_model_exclude_none=True)
async def get_all_scopes(params: Params = Depends(), role_id: int = None):
    if role_id:
        scopes = Scope.objects.select_related("roles").filter(roles__id=role_id)
        if not len(scopes):
            raise RoleScopeNotFound()
    else:
        scopes = Scope.objects
    return await paginate(scopes, params)
