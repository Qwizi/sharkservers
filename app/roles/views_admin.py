from asyncpg import UniqueViolationError
from fastapi import APIRouter, Security, Depends, HTTPException
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.ormar import paginate
from ormar import NoMatch
from psycopg2 import IntegrityError
from sqlite3 import IntegrityError as SQLIntegrityError

from app.auth.utils import get_admin_user
from app.roles.exceptions import RoleNotFound, RoleExists
from app.roles.models import Role
from app.roles.schemas import RoleOut, RoleOutWithScopes, CreateRole
from app.scopes.models import Scope
from app.users.models import User

router = APIRouter()


@router.get("", response_model=Page[RoleOut])
async def admin_get_roles(params: Params = Depends(), user: User = Security(get_admin_user, scopes=["roles:get_all"])):
    roles = Role.objects
    return await paginate(roles, params)


@router.get("/{role_id}", response_model=RoleOutWithScopes)
async def admin_get_role(role_id: int, user: User = Security(get_admin_user, scopes=["roles:retrieve"])):
    try:
        role = await Role.objects.select_related("scopes").get(id=role_id)
        return role
    except NoMatch:
        raise RoleNotFound()


@router.post("", response_model=RoleOutWithScopes)
async def admin_create_role(role_data: CreateRole, user: User = Security(get_admin_user, scopes=["roles:create"])):
    scopes = None
    if role_data.scopes:
        scopes = await Scope.objects.filter(id__in=role_data.scopes).all()
        print(scopes)
    try:
        role = await Role.objects.create(
            name=role_data.name,
            color=role_data.color,
            is_staff=role_data.is_staff
        )
        if scopes:
            for scope in scopes:
                await role.scopes.add(scope)
        return role
    except UniqueViolationError as e:
        raise RoleExists


@router.delete("/{role_id}")
async def admin_delete_role(role_id: int, user: User = Security(get_admin_user, scopes=["roles:delete"])):
    protected_role_ids = [1, 2, 3]
    if role_id in protected_role_ids:
        raise HTTPException(detail="U cannot delete protected role", status_code=400)
    try:
        role = await Role.objects.get(id=role_id)
    except NoMatch:
        raise RoleNotFound
