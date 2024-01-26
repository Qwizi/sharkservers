"""Dependencies for roles module."""

from fastapi import Depends
from ormar import Model

from sharkservers.roles.services import RoleService


async def get_roles_service() -> RoleService:
    """Get the RoleService instance."""
    return RoleService()


async def get_valid_role(
    role_id: int,
    roles_service: RoleService = Depends(get_roles_service),
) -> Model:
    """
    Get a valid role by its ID.

    Args:
    ----
        role_id (int): The ID of the role.
        roles_service (RoleService, optional): The RoleService instance to use. Defaults to Depends(get_roles_service).

    Returns:
    -------
        Model: The valid role model.

    """
    return await roles_service.get_one(id=role_id, related=["scopes"])
