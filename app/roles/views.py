from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params, paginate
from ormar import NoMatch

from app.roles.exceptions import RoleNotFound
from app.roles.models import Role
from app.roles.schemas import RoleOut, RoleOutWithScopes

router = APIRouter()


@router.get("", response_model=Page[RoleOut], response_model_exclude_none=True)
async def get_roles(params: Params = Depends()):
    roles = await Role.objects.all()
    return paginate(roles, params)


@router.get("/{role_id}", response_model=RoleOutWithScopes)
async def get_user(role_id: int):
    try:
        user = await Role.objects.select_related("scopes").get(id=role_id)
        return user
    except NoMatch as e:
        raise RoleNotFound()
