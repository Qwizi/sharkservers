from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate, Params

from app.scopes.exceptions import RoleScopeNotFound
from app.scopes.models import Scope
from app.scopes.schemas import ScopeOut

router = APIRouter()


@router.get("", response_model=Page[ScopeOut], response_model_exclude_none=True)
async def get_all_scopes(params: Params = Depends(), role_id: int = None):
    if role_id:
        scopes = await Scope.objects.select_related("roles").filter(roles__id=role_id).all()
        if not len(scopes):
            raise RoleScopeNotFound()
    else:
        scopes = await Scope.objects.all()
    return paginate(scopes, params)
