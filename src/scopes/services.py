import os
from typing import List

from src.db import BaseService
from src.roles.models import Role
from src.scopes.enums import ScopeEnum
from src.scopes.exceptions import scope_not_found_exception
from src.scopes.models import Scope
from src.scopes.schemas import CreateScopeSchema


class ScopeService(BaseService):
    extra_scopes: list[CreateScopeSchema] | None
    default_scopes: list[str]

    def __init__(self, model, not_found_exception):
        super().__init__(model, not_found_exception)
        self.extra_scopes = None
        self.default_scopes = []

    def add_default_scopes(self, apps: list[str]):
        """
        Add default scope
        :param apps:
        :return:
        """
        for app in apps:
            self.default_scopes.append(app)
        return self

    def add_extra_scope(self, app_name: str, scope_values: list[tuple[str, str, str]]):
        """
        Add extra scope
        :param scope_values:
        :param app_name:
        :return:
        """
        if not self.extra_scopes:
            self.extra_scopes = []
        for scope_value in scope_values:
            app_name = scope_value[0]
            value = scope_value[1]
            description = scope_value[2]
            self.extra_scopes.append(CreateScopeSchema(app_name=app_name, value=value, description=description))
        return self

    def get_extra_scopes(self) -> list[CreateScopeSchema]:
        """
        Get extra scopes
        :return:
        """
        return self.extra_scopes or []

    async def create_scopes_for_app(self, app_name: str, additional_scopes: list[tuple[str, str, str]]):
        """
        Create scopes for app
        :param additional_scopes:
        :param app_name:
        :return:
        """
        for scope_enum in ScopeEnum:
            scope, created = await self.model.objects.get_or_create(
                app_name=app_name,
                value=scope_enum.value,
                description=f"{scope_enum.value} {app_name}s".capitalize(),
                protected=True
            )
        for scope in additional_scopes:
            _app_name, value, description = scope
            additional_scope, additional_scope_created = await self.model.objects.get_or_create(
                app_name=_app_name,
                value=value,
                description=description,
            )

    async def create_default_scopes(self, applications, additional=None):
        """
        :param applications:
        :param additional:
        :return:
        """
        for app in applications:
            await self.create_scopes_for_app(app, additional)

    @staticmethod
    async def get_scopes_list(roles: list[Role]):
        """
        Get scopes list
        :return:
        """
        scopes = []
        for role in roles:
            for scope in role.scopes:
                scope_str = scope.get_string()
                if scope_str not in scopes:
                    scopes.append(scope.get_string())
        return scopes


scopes_service = ScopeService(Scope, not_found_exception=scope_not_found_exception)