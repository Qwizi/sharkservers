from src.db import BaseService
from src.logger import logger_with_filename
from src.roles.enums import ProtectedDefaultRolesEnum
from src.roles.exceptions import role_not_found_exception
from src.roles.models import Role
from src.roles.schemas import CreateRoleSchema
from src.scopes.services import ScopeService


class RoleService(BaseService):
    class Meta:
        model = Role
        not_found_exception = role_not_found_exception

    async def create_default_roles(self, scopes_service: ScopeService):
        roles_to_create = [
            (ProtectedDefaultRolesEnum.ADMIN.value, "Admin", "#C53030"),
            (ProtectedDefaultRolesEnum.USER.value, "User", "#99999"),
            (ProtectedDefaultRolesEnum.BANNED.value, "Banned", "#000000"),
        ]
        for role in roles_to_create:
            logger_with_filename(filename=self.__class__.__name__, data=role)
            default_role, created = await self.Meta.model.objects.get_or_create(
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
                    await default_role.scopes.add(scope)

    async def get_staff_roles(self, params):
        return await self.get_all(params=params, related=["user_display_role"], is_staff=True)

    async def admin_create_role(self, role_data: CreateRoleSchema, scopes_service: ScopeService) -> Role:
        """ Create role with scopes """
        scopes = []
        role_data_dict = role_data.dict()
        scopes_from_role_data = role_data_dict.pop("scopes", None)
        if scopes_from_role_data:
            scopes = await scopes_service.Meta.model.objects.filter(id__in=role_data.scopes).all()
        role = await self.create(**role_data_dict)
        if scopes:
            for scope in scopes:
                await role.scopes.add(scope)
        return role
