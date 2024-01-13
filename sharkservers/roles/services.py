"""Services for roles."""
from __future__ import annotations

from typing import TYPE_CHECKING

from sharkservers.db import BaseService
from sharkservers.logger import logger_with_filename
from sharkservers.roles.enums import ProtectedDefaultRolesTagEnum
from sharkservers.roles.exceptions import role_not_found_exception
from sharkservers.roles.models import Role

if TYPE_CHECKING:
    from fastapi_pagination import Page, Params

    from sharkservers.roles.schemas import CreateRoleSchema
    from sharkservers.scopes.services import ScopeService


class RoleService(BaseService):
    """
    Service class for managing roles.

    Attributes
    ----------
        create_default_roles (Callable): Creates default roles with specified scopes.
        get_staff_roles (Callable): Retrieves staff roles.
        admin_create_role (Callable): Creates a role with specified scopes.

    """

    class Meta:
        """RoleService metadata."""

        model = Role
        not_found_exception = role_not_found_exception

    async def create_default_roles(self, scopes_service: ScopeService) -> None:
        """
        Creates default roles with specified scopes.

        Args:
        ----
            scopes_service (ScopeService): The service for managing scopes.
        """  # noqa: D401
        roles_to_create: list[tuple[ProtectedDefaultRolesTagEnum, str]] = [
            (ProtectedDefaultRolesTagEnum.ADMIN.value, "Admin", "#C53030"),
            (ProtectedDefaultRolesTagEnum.USER.value, "User", "#99999"),
            (ProtectedDefaultRolesTagEnum.BANNED.value, "Banned", "#000000"),
            (ProtectedDefaultRolesTagEnum.VIP.value, "VIP", "#ffda83"),
        ]
        for role in roles_to_create:
            logger_with_filename(filename=self.__class__.__name__, data=role)
            if not await self.Meta.model.objects.filter(tag=role[0]).exists():
                default_role = await self.Meta.model.objects.create(
                    tag=role[0],
                    name=role[1],
                    color=role[2],
                    is_staff=role[0] == ProtectedDefaultRolesTagEnum.ADMIN.value,
                )
                scopes = await scopes_service.get_default_scopes_for_role(
                    role_id=default_role.id,
                )
                if role[0] != ProtectedDefaultRolesTagEnum.BANNED.value:
                    for scope in scopes:
                        await default_role.scopes.add(scope)

    async def get_staff_roles(self, params: Params) -> Page[Role]:
        """
        Retrieves staff roles.

        Args:
        ----
            params: Additional parameters for filtering or pagination.

        Returns:
        -------
            List: A list of staff roles.
        """  # noqa: D401
        return await self.get_all(
            params=params,
            related=["user_display_role"],
            is_staff=True,
        )

    async def admin_create_role(
        self,
        role_data: CreateRoleSchema,
        scopes_service: ScopeService,
    ) -> Role:
        """
        Create a role with specified scopes.

        Args:
        ----
            role_data (CreateRoleSchema): The data for creating the role.
            scopes_service (ScopeService): The service for managing scopes.

        Returns:
        -------
            Role: The created role.
        """
        scopes = []
        role_data_dict = role_data.dict()
        scopes_from_role_data = role_data_dict.pop("scopes", None)
        if scopes_from_role_data:
            scopes = await scopes_service.Meta.model.objects.filter(
                id__in=role_data.scopes,
            ).all()
        role = await self.create(**role_data_dict)
        if scopes:
            for scope in scopes:
                await role.scopes.add(scope)
        return role
