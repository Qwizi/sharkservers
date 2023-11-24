from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from src.admins.dependencies import get_groups_service, get_valid_group
from src.admins.models import Group
from src.admins.schemas import CreateGroupSchema, GroupOut

from src.admins.services import GroupService


router = APIRouter()

@router.get("/")
async def get_groups(
    params: Params = Depends(),
    groups_service: GroupService = Depends(get_groups_service)
) -> Page[GroupOut]:
    return await groups_service.get_all(params=params)

@router.post("/")
async def create_group(
    data: CreateGroupSchema,
    groups_service: GroupService = Depends(get_groups_service)
) -> GroupOut:
    return await groups_service.create(**data.dict())

@router.get("/{group_id}")
async def get_group(
    group: Group = Depends(get_valid_group)
) -> GroupOut:
    return group


@router.delete("/{group_id}")
async def delete_group(
    group: Group = Depends(get_valid_group)
) -> GroupOut:
    await group.delete()
    return group