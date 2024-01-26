"""Servers models."""
from __future__ import annotations

import ormar
from fastapi_pagination import Params
from sourcemod_api_client import (
    AdminOut,
    APIConfig,
    CreateAdminSchema,
    GroupOut,
    Page_AdminOut_,
    Page_GroupOut_,
    UpdateAdminSchema,
)
from sourcemod_api_client.models.CreateGroupSchema import CreateGroupSchema
from sourcemod_api_client.services.async_admins_groups_service import (
    admins_groups_create_group,
    admins_groups_delete_group,
    admins_groups_get_group,
    admins_groups_get_groups,
)
from sourcemod_api_client.services.async_adminss_service import (
    adminss_create_admin,
    adminss_delete_admin,
    adminss_get_admin,
    adminss_get_admins,
    adminss_update_admin,
)

from sharkservers.db import BaseMeta, DateFieldsMixins
from sharkservers.logger import logger
from sharkservers.roles.dependencies import get_roles_service
from sharkservers.roles.enums import ProtectedDefaultRolesEnum
from sharkservers.roles.models import Role
from sharkservers.roles.schemas import RoleOut
from sharkservers.scopes.dependencies import get_scopes_service


class Server(ormar.Model, DateFieldsMixins):
    """
    Represents a server in the system.

    Attributes
    ----------
        id (int): The unique identifier of the server.
        name (str, optional): The name of the server.
        tag (str, optional): The tag of the server.
        ip (str, optional): The IP address of the server.
        port (int, optional): The port number of the server.
        admin_role (Role, optional): The admin role associated with the server.
        api_url (str, optional): The API URL of the server.

    Methods
    -------
        get_sourcemod_api_config(): Returns the APIConfig object for the server's Sourcemod API.
        get_admins_groups(params: Params) -> Page_GroupOut_: Retrieves a page of admin groups for the server.
        get_admin_group(group_id: int): Retrieves an admin group by its ID.
        create_admin_group(data: CreateGroupSchema): Creates a new admin group for the server.
        delete_admin_group(group_id: int): Deletes an admin group by its ID.
        get_admins(params: Params): Retrieves a page of admins for the server.
        get_admin(identity: str): Retrieves an admin by their identity.
        create_admin(data: CreateAdminSchema): Creates a new admin for the server.
        update_admin(identity: str, data: UpdateAdminSchema): Updates an admin by their identity.
        delete_admin(identity: str): Deletes an admin by their identity.
    """

    class Meta(BaseMeta):
        """Metadata for the server model."""

        tablename = "servers"

    id: int = ormar.Integer(primary_key=True)
    name: str | None = ormar.String(max_length=64)
    tag: str | None = ormar.String(max_length=64, unique=True)
    ip: str | None = ormar.String(max_length=64)
    port: int | None = ormar.Integer()
    admin_role: Role | None = ormar.ForeignKey(Role)
    api_url: str | None = ormar.String(max_length=256)

    def get_sourcemod_api_config(self) -> APIConfig:
        """
        Return the APIConfig object for the server's Sourcemod API.

        Returns
        -------
            APIConfig: The APIConfig object for the server's Sourcemod API.
        """
        return APIConfig(
            base_path=self.api_url,
        )

    async def get_admins_groups(self, params: Params) -> Page_GroupOut_:
        """
        Get a page of admin groups for the server.

        Args:
        ----
            params (Params): The pagination parameters.

        Returns:
        -------
            Page_GroupOut_: The page of admin groups for the server.
        """
        return await admins_groups_get_groups(
            api_config_override=self.get_sourcemod_api_config(),
            page=params.page,
            size=params.size,
        )

    async def get_admin_group(self, group_id: int) -> GroupOut:
        """
        Get an admin group by its ID.

        Args:
        ----
            group_id (int): The ID of the admin group.

        Returns:
        -------
            GroupOut: The admin group.
        """
        return admins_groups_get_group(
            group_id=group_id,
            api_config_override=self.get_sourcemod_api_config(),
        )

    async def create_admin_group(self, data: CreateGroupSchema) -> GroupOut:
        """
        Create a new admin group for the server.

        Args:
        ----
            data (CreateGroupSchema): The data for the new admin group.

        Returns:
        -------
            GroupOut: The newly created admin group.
        """
        return await admins_groups_create_group(
            data=data,
            api_config_override=self.get_sourcemod_api_config(),
        )

    async def delete_admin_group(self, group_id: int) -> GroupOut:
        """
        Delete an admin group by its ID.

        Args:
        ----
            group_id (int): The ID of the admin group.

        Returns:
        -------
            GroupOut: The deleted admin group.
        """
        return await admins_groups_delete_group(
            group_id=group_id,
            api_config_override=self.get_sourcemod_api_config(),
        )

    async def get_admins(self, params: Params) -> Page_AdminOut_:
        """
        Get a page of admins for the server.

        Args:
        ----
            params (Params): The pagination parameters.

        Returns:
        -------
            Page_AdminOut_: The page of admins for the server.
        """
        return await adminss_get_admins(
            api_config_override=self.get_sourcemod_api_config(),
            page=params.page,
            size=params.size,
        )

    async def get_admin(self, identity: str) -> AdminOut:
        """
        Get an admin by their identity.

        Args:
        ----
            identity (str): The identity of the admin.
        """
        return await adminss_get_admin(
            identity=identity,
            api_config_override=self.get_sourcemod_api_config(),
        )

    async def create_admin(self, data: CreateAdminSchema) -> AdminOut:
        """
        Create a new admin for the server.

        Args:
        ----
            data (CreateAdminSchema): The data for the new admin.

        Returns:
        -------
            AdminOut: The newly created admin.
        """
        return await adminss_create_admin(
            data=data,
            api_config_override=self.get_sourcemod_api_config(),
        )

    async def update_admin(self, identity: str, data: UpdateAdminSchema) -> AdminOut:
        """
        Update an admin by their identity.

        Args:
        ----
            identity (str): The identity of the admin.
            data (UpdateAdminSchema): The data to update the admin with.

        Returns:
        -------
            AdminOut: The updated admin.
        """
        return await adminss_update_admin(
            identity=identity,
            data=data,
            api_config_override=self.get_sourcemod_api_config(),
        )

    async def delete_admin(self, identity: str) -> AdminOut:
        """
        Delete an admin by their identity.

        Args:
        ----
            identity (str): The identity of the admin.

        Returns:
        -------
            AdminOut: The deleted admin.
        """
        return await adminss_delete_admin(
            identity=identity,
            api_config_override=self.get_sourcemod_api_config(),
        )


async def create_admin_role(instance: Server) -> RoleOut:
    """
    Create an admin role for the server.

    Args:
    ----
        instance (Server): The server instance.

    Returns:
    -------
        Role: The newly created admin role.
    """
    roles_service = await get_roles_service()
    scopes_service = await get_scopes_service()
    role_name = f"Admin {instance.name.capitalize()}"
    logger.info(role_name)
    scopes = await scopes_service.get_default_scopes_for_role(
        ProtectedDefaultRolesEnum.USER.value,
    )
    logger.info(scopes)

    new_admin_role = await roles_service.create(
        tag=role_name.replace(" ", "_").lower(),
        name=role_name,
        color="#fea501",
        is_staff=True,
    )
    for scope in scopes:
        await new_admin_role.scopes.add(scope)
    return new_admin_role


@ormar.post_save(Server)
async def on_server_created(
    sender: Server, instance: Server, **kwargs
) -> None:  # noqa: ANN003, ARG001
    """
    On server created event.

    Args:
    ----
        sender (Server): The sender of the event.
        instance (Server): The server instance.
        **kwargs: The keyword arguments.

    Returns:
    -------
        None
    """
    new_admin_role = await create_admin_role(instance)
    await instance.update(admin_role=new_admin_role)
    await instance.create_admin_group(
        data=CreateGroupSchema(
            name="Admin",
            immunity_level=100,
            flags="z",
        ),
    )


@ormar.post_delete(Server)
async def on_server_deleted(
    sender, instance: Server, **kwargs
) -> None:  # noqa: ANN001, ARG001, ANN003
    """
    On server deleted event.

    Args:
    ----
        sender (Server): The sender of the event.
        instance (Server): The server instance.
        **kwargs: The keyword arguments.
    """
    await instance.admin_role.delete()
    admins_groups = await instance.get_admins_groups(params=Params())
    admins = await instance.get_admins(params=Params())
    for admin_group in admins_groups.items:
        await instance.delete_admin_group(group_id=admin_group.id)

    for admin in admins.items:
        await instance.delete_admin(identity=admin.identity)
