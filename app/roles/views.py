from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.ormar import paginate

from ormar import NoMatch, or_, and_

from app.roles.exceptions import RoleNotFound
from app.roles.models import Role
from app.roles.schemas import RoleOut, RoleOutWithScopes, RoleOutWithoutScopesAndUserRoles, StaffRoles

router = APIRouter()


@router.get("", response_model=Page[RoleOut], response_model_exclude_none=True)
async def get_roles(params: Params = Depends()):
    return await paginate(Role.objects, params)


@router.get("/staff", response_model=Page[StaffRoles], response_model_exclude={"password"})
async def get_staff_roles():
    roles = await Role.objects.select_related(
        ["user_display_role"]).filter(
        is_staff=True
    ) \
        .all()
    # I need fix this
    return {
        "items": roles,
        "total": len(roles),
        "page": 1,
        "size": 50
    }


@router.get("/{role_id}", response_model=RoleOutWithScopes)
async def get_user(role_id: int):
    try:
        user = await Role.objects.select_related("scopes").get(id=role_id)
        return user
    except NoMatch as e:
        raise RoleNotFound()
