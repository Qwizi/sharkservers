
from xml.dom.minidom import Identified
from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params

from src.admins.dependencies import get_admins_service, get_valid_admin, get_valid_group
from src.admins.models import Admin
from src.admins.schemas import AdminOut, CreateAdminSchema, UpdateAdminSchema
from src.admins.services import AdminService
from src.admins.dependencies import get_groups_service
from src.admins.services import GroupService

router = APIRouter()


@router.get("/")
async def get_admins(
    params: Params = Depends(),
    admin_service: AdminService = Depends(get_admins_service)
) -> Page[AdminOut]:
    admins = await admin_service.get_all(params=params, related=["groups"])
    return admins


@router.get("/{identity}")
async def get_admin(
    admin: Admin = Depends(get_valid_admin)
) -> AdminOut:
    return admin

@router.post("/")
async def create_admin(
    data: CreateAdminSchema,
    admins_service: AdminService = Depends(get_admins_service),
    groups_service: GroupService = Depends(get_groups_service)
):
    groups_list = []
    if data.groups_id:
        for group_id in data.groups_id:
            group = await get_valid_group(group_id=group_id, group_service=groups_service)
            groups_list.append(group)
    new_admin = await admins_service._create(data, groups_list=groups_list if groups_list else None)
    return new_admin

@router.put("/{identity}")
async def update_admin(
    updated_data: UpdateAdminSchema,
    admin: Admin = Depends(get_valid_admin),
    admins_service: AdminService = Depends(get_admins_service),
    groups_service: GroupService = Depends(get_groups_service)
):
    groups_list = []
    if updated_data.groups_id:
        for group_id in updated_data.groups_id:
            group = await get_valid_group(group_id=group_id, group_service=groups_service)
            groups_list.append(group)
    updated_admin = await admins_service._update(admin, updated_data=updated_data, groups_list=groups_list if groups_list else None)
    return updated_admin

@router.delete("/{identity}")
async def delete_admin(
    admin: Admin = Depends(get_valid_admin)
):
    await admin.delete()
    return admin