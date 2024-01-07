from fastapi import Depends
from ormar import Model
from src.roles.services import RoleService


async def get_roles_service() -> RoleService:
    return RoleService()


async def get_valid_role(
    role_id: int, roles_service: RoleService = Depends(get_roles_service)
) -> Model:
    return await roles_service.get_one(id=role_id, related=["scopes"])
