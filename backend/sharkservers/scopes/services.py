"""Scopes services."""
from __future__ import annotations

from typing import TYPE_CHECKING

from ormar import and_, or_

from sharkservers.db import BaseService
from sharkservers.roles.enums import ProtectedDefaultRolesTagEnum
from sharkservers.scopes.enums import ScopeEnum
from sharkservers.scopes.exceptions import scope_not_found_exception
from sharkservers.scopes.models import Scope
from sharkservers.scopes.schemas import CreateScopeSchema

if TYPE_CHECKING:
    from sharkservers.roles.models import Role


class ScopeService(BaseService):
    """
    Service class for managing scopes.

    Attributes
    ----------
    extra_scopes : list[CreateScopeSchema] | None
        List of extra scopes.
    default_scopes : list[str]
        List of default scopes.

    Methods
    -------
        add_default_scopes(apps)
            Add default scope.
        add_extra_scope(app_name, scope_values)
            Add extra scope.
        get_extra_scopes()
            Get extra scopes.
        create_scopes_for_app(app_name, additional_scopes)
            Create scopes for app.
        create_default_scopes(applications, additional=None)
            Create default scopes for applications.
        get_scopes_list(roles)
            Get list of scopes for the given roles.
        get_default_scopes_for_role(role_id)
            Get default scopes for the given role.
    """

    extra_scopes: list[CreateScopeSchema] | None
    default_scopes: list[str]

    class Meta:
        """Meta class for ScopeService."""

        model = Scope
        not_found_exception = scope_not_found_exception

    def add_default_scopes(self, apps: list[str]) -> ScopeService:
        """
        Add default scope.

        Args:
        ----
        apps : list[str]
            List of application names.

        Returns:
        -------
        ScopeService
            The ScopeService instance.

        """
        for app in apps:
            self.default_scopes.append(app)
        return self

    def add_extra_scope(
        self,
        app_name: str,
        scope_values: list[tuple[str, str, str]],
    ) -> ScopeService:
        """
        Add extra scope.

        Parameters
        ----------
        app_name : str
            Name of the application.
        scope_values : list[tuple[str, str, str]]
            List of tuples containing scope values.

        Returns
        -------
        ScopeService
            The ScopeService instance.

        """
        if not self.extra_scopes:
            self.extra_scopes = []
        for scope_value in scope_values:
            app_name = scope_value[0]
            value = scope_value[1]
            description = scope_value[2]
            self.extra_scopes.append(
                CreateScopeSchema(
                    app_name=app_name,
                    value=value,
                    description=description,
                ),
            )
        return self

    def get_extra_scopes(self) -> list[CreateScopeSchema]:
        """
        Get extra scopes.

        Returns
        -------
        list[CreateScopeSchema]
            List of extra scopes.

        """
        return self.extra_scopes or []

    async def create_scopes_for_app(
        self,
        app_name: str,
        additional_scopes: list[tuple[str, str, str]],
    ) -> None:
        """
        Create scopes for app.

        Args:
        ----
        app_name : str
            Name of the application.
        additional_scopes : list[tuple[str, str, str]]
            List of tuples containing additional scope values.

        Returns:
        -------
        None

        """
        for scope_enum in ScopeEnum:
            scope, created = await self.Meta.model.objects.get_or_create(
                app_name=app_name,
                value=scope_enum.value,
                description=f"{scope_enum.value} {app_name}s".capitalize(),
                protected=True,
            )
        for scope in additional_scopes:
            _app_name, value, description = scope
            (
                additional_scope,
                additional_scope_created,
            ) = await self.Meta.model.objects.get_or_create(
                app_name=_app_name,
                value=value,
                description=description,
            )

    async def create_default_scopes(
        self,
        applications,  # noqa: ANN001
        additional=None,  # noqa: ANN001
    ) -> None:
        """
        Create default scopes for applications.

        Parameters
        ----------
        applications : list
            List of application names.
        additional : list, optional
            List of additional scope values, by default None.

        Returns
        -------
        None

        """
        for app in applications:
            # Code for creating default scopes goes here
            await self.create_scopes_for_app(app, additional)

    @staticmethod
    async def get_scopes_list(roles: list[Role]) -> list[str]:
        """
        Get list of scopes for the given roles.

        Args:
        ----
        roles : list[Role]
            List of roles.

        Returns:
        -------
        list
            List of scopes.

        """
        scopes = []
        for role in roles:
            if role.id == ProtectedDefaultRolesTagEnum.BANNED.value:
                return []
            for scope in role.scopes:
                scope_str = scope.get_string()
                if scope_str not in scopes:
                    scopes.append(scope.get_string())
        return scopes

    async def get_default_scopes_for_role(self, role_tag: str) -> list[Scope]:
        """
        Get default scopes for the given role.

        Args:
        ----
        role_tag : str
            Role tag.

        Returns:
        -------
        list
            List of default scopes.

        """
        scopes = None
        if role_tag == ProtectedDefaultRolesTagEnum.ADMIN.value:
            scopes = await self.Meta.model.objects.all()
        elif role_tag in (
            ProtectedDefaultRolesTagEnum.USER.value,
            ProtectedDefaultRolesTagEnum.VIP.value,
        ):
            scopes = await self.Meta.model.objects.filter(
                or_(
                    and_(app_name="users", value="me"),
                    and_(app_name="users", value="me:username"),
                    and_(app_name="users", value="me:password"),
                    and_(app_name="users", value="me:display-role"),
                    and_(app_name="threads", value="create"),
                    and_(app_name="threads", value="update"),
                    and_(app_name="posts", value="create"),
                    and_(app_name="posts", value="update"),
                ),
            ).all()
        return scopes
