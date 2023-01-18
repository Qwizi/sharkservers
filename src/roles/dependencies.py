from src.roles.models import Role
from src.roles.services import roles_service


async def get_valid_role(role_id: int) -> Role:
    return await roles_service.get_one(id=role_id, related=["scopes"])
