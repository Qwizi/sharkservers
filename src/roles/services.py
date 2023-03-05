from src.db import BaseService
from src.logger import logger_with_filename
from src.roles.enums import ProtectedDefaultRolesEnum
from src.roles.exceptions import role_not_found_exception
from src.roles.models import Role
from src.scopes.services import ScopeService


class RoleService(BaseService):
    async def create_default_roles(self, scopes_service: ScopeService):
        roles_to_create = [
            (ProtectedDefaultRolesEnum.ADMIN.value, "Admin", "#C53030"),
            (ProtectedDefaultRolesEnum.USER.value, "User", "#99999"),
            (ProtectedDefaultRolesEnum.BANNED.value, "Banned", "#000000"),
        ]
        for role in roles_to_create:
            logger_with_filename(filename=__file__, data=role)
            default_role, created = await self.model.objects.get_or_create(
                id=role[0],
                name=role[1],
                color=role[2],
                is_staff=True
                if role[0] == ProtectedDefaultRolesEnum.ADMIN.value
                else False,
            )
            scopes = await scopes_service.get_default_scopes_for_role(
                role_id=default_role.id
            )
            if not role[0] == ProtectedDefaultRolesEnum.BANNED.value:
                for scope in scopes:
                    logger_with_filename(filename=__file__, data=scope)
                    await default_role.scopes.add(scope)


roles_service = RoleService(Role, not_found_exception=role_not_found_exception)
