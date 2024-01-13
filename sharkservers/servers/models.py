from typing import Optional

import ormar
from fastapi_pagination import Params
from pydantic.color import Color
from sourcemod_api_client import (
    APIConfig,
    CreateAdminSchema,
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
from sharkservers.players.models import Player
from sharkservers.roles.dependencies import get_roles_service
from sharkservers.roles.enums import ProtectedDefaultRolesEnum
from sharkservers.roles.models import Role
from sharkservers.scopes.dependencies import get_scopes_service


class Server(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "servers"

    id: int = ormar.Integer(primary_key=True)
    name: Optional[str] = ormar.String(max_length=64)
    tag: Optional[str] = ormar.String(max_length=64, unique=True)
    ip: Optional[str] = ormar.String(max_length=64)
    port: Optional[str] = ormar.Integer()
    admin_role: Optional[Role] = ormar.ForeignKey(Role)
    api_url: Optional[str] = ormar.String(max_length=256)

    def get_sourcemod_api_config(self):
        return APIConfig(
            base_path=self.api_url,
        )

    async def get_admins_groups(self, params: Params) -> Page_GroupOut_:
        return await admins_groups_get_groups(
            api_config_override=self.get_sourcemod_api_config(),
            page=params.page,
            size=params.size,
        )

    async def get_admin_group(self, group_id: int):
        return admins_groups_get_group(
            group_id=group_id,
            api_config_override=self.get_sourcemod_api_config(),
        )

    async def create_admin_group(self, data: CreateGroupSchema):
        return await admins_groups_create_group(
            data=data,
            api_config_override=self.get_sourcemod_api_config(),
        )

    async def delete_admin_group(self, group_id: int):
        return await admins_groups_delete_group(
            group_id=group_id,
            api_config_override=self.get_sourcemod_api_config(),
        )

    async def get_admins(self, params: Params):
        return await adminss_get_admins(
            api_config_override=self.get_sourcemod_api_config(),
            page=params.page,
            size=params.size,
        )

    async def get_admin(self, identity: str):
        return await adminss_get_admin(
            identity=identity,
            api_config_override=self.get_sourcemod_api_config(),
        )

    async def create_admin(self, data: CreateAdminSchema):
        return await adminss_create_admin(
            data=data,
            api_config_override=self.get_sourcemod_api_config(),
        )

    async def update_admin(self, identity: str, data: UpdateAdminSchema):
        return await adminss_update_admin(
            identity=identity,
            data=data,
            api_config_override=self.get_sourcemod_api_config(),
        )

    async def delete_admin(self, identity: str):
        return await adminss_delete_admin(
            identity=identity,
            api_config_override=self.get_sourcemod_api_config(),
        )


class ChatColorModule(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "chat_color_module"

    id: int = ormar.Integer(primary_key=True)
    server: Server = ormar.ForeignKey(Server, related_name="server_chat_color_module")
    player: Optional[Player] = ormar.ForeignKey(
        Player,
        related_name="player_chat_color_module",
        nullable=True,
    )
    tag: str = ormar.String(max_length=64, unique=True)
    flag: Optional[str] = ormar.String(max_length=1, unique=True)
    tag_color: Color = ormar.String(max_length=8)
    name_color: Color = ormar.String(max_length=8)
    text_color: Color = ormar.String(max_length=8)


async def create_admin_role(instance: Server):
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
async def on_server_created(sender, instance: Server, **kwargs):
    new_admin_role = await create_admin_role(instance)
    await instance.update(admin_role=new_admin_role)
    admins_groups = await instance.create_admin_group(
        data=CreateGroupSchema(
            name="Admin",
            immunity_level=100,
            flags="z",
        ),
    )
    print(admins_groups)


@ormar.post_delete(Server)
async def on_server_deleted(sender, instance: Server, **kwargs):
    await instance.admin_role.delete()
    admins_groups = await instance.get_admins_groups(params=Params())
    admins = await instance.get_admins(params=Params())
    for admin_group in admins_groups.items:
        await instance.delete_admin_group(group_id=admin_group.id)

    for admin in admins.items:
        await instance.delete_admin(identity=admin.identity)


"""
@post_save(Server)
async def create_roles_after_server_creation(sender, instance, **kwargs):
    logger.info("Creating roles for server %s", instance.name)
    roles_service = await get_roles_service()
    scopes_service = await get_scopes_service()

    server_admin_role_name = f"Admin {instance.name}".capitalize()
    server_patron_role_name = f"Opiekun {instance.name}".capitalize()
    roles = [server_admin_role_name, server_patron_role_name]
    user_role_scopes = await scopes_service.get_default_scopes_for_role(
        ProtectedDefaultRolesEnum.USER.value
    )
    for role_name in roles:
        role_obj, created = await roles_service.Meta.model.objects.get_or_create(
            name=role_name,
            _defaults={
                "name": role_name,
                "color": "#fea500"
                if role_name == server_admin_role_name
                else "#a500ff",
                "is_staff": True,
            },
        )
        if created:
            for scope in user_role_scopes:
                await role_obj.scopes.add(scope)
        logger.info(role_name, created, role_obj)


@post_save(Server)
async def create_default_chat_tags(sender, instance, **kwargs):
    logger.info("Creating default chat tags for server %s", instance.name)
    tags = [
        ChatColorModule(
            server=instance,
            tag="[Owner]",
            flag="z",
            tag_color="#ff0000",
            name_color="#ff0000",
            text_color="#ff0000",
        ),
        ChatColorModule(
            server=instance,
            tag="[Admin]",
            flag="k",
            tag_color="#fea500",
            name_color="#fea500",
            text_color="#fea500",
        ),
        ChatColorModule(
            server=instance,
            tag="[Opiekun]",
            flag="o",
            tag_color="#a500ff",
            name_color="#a500ff",
            text_color="#a500ff",
        ),
        ChatColorModule(
            server=instance,
            tag="[Shark]",
            flag="s",
            tag_color="#00ff00",
            name_color="#00ff00",
            text_color="#00ff00",
        ),
    ]

    for tag in tags:
        await tag.save()
"""
