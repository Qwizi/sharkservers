from enum import unique
from re import L
from typing import Optional

import ormar
from pydantic.color import Color
from src.settings import get_settings
from src.roles.enums import ProtectedDefaultRolesEnum
from src.roles.dependencies import get_roles_service
from src.scopes.dependencies import get_scopes_service
from src.roles.models import Role

from src.db import BaseMeta, DateFieldsMixins
from src.players.models import Player
from src.roles.models import Role
from src.logger import logger

from sourcemod_api_client import APIConfig
from sourcemod_api_client.services.async_admins_groups_service import (
    admins_groups_create_group,
)
from sourcemod_api_client.models.CreateGroupSchema import CreateGroupSchema


class Server(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "servers"

    id: int = ormar.Integer(primary_key=True)
    name: Optional[str] = ormar.String(max_length=64)
    tag: Optional[str] = ormar.String(max_length=64, unique=True)
    ip: Optional[str] = ormar.String(max_length=64)
    port: Optional[str] = ormar.Integer()
    admin_role: Optional[Role] = ormar.ForeignKey(Role)


"""
class ServerPlayerStats(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "server_stats"

    id: int = ormar.Integer(primary_key=True)
    server: Server = ormar.ForeignKey(Server, related_name="server_stats")
    player: Player = ormar.ForeignKey(Player, related_name="player_stats")
    stats: list[PlayerStats] = ormar.ManyToMany(PlayerStats, related_name="stats")
    points: int = ormar.Integer(default=1000)
"""


class ChatColorModule(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "chat_color_module"

    id: int = ormar.Integer(primary_key=True)
    server: Server = ormar.ForeignKey(Server, related_name="server_chat_color_module")
    player: Optional[Player] = ormar.ForeignKey(
        Player, related_name="player_chat_color_module", nullable=True
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
        ProtectedDefaultRolesEnum.USER.value
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


async def create_sourcemod_server_admin_group(instance: Server):
    settings = get_settings()
    api_url = None
    for api in settings.SOURCEMOD_API_URLS:
        if api["tag"] == instance.tag:
            api_url = api["url"]
            break

    api_config = APIConfig(
        base_path=api_url,
    )
    return await admins_groups_create_group(
        data=CreateGroupSchema(
            name=f"Admin",
            immunity_level=100,
            flags="z",
        ),
        api_config_override=api_config,
    )


@ormar.post_save(Server)
async def on_server_created(sender, instance: Server, **kwargs):
    new_admin_role = await create_admin_role(instance)
    await instance.update(admin_role=new_admin_role)
    admins_groups = await create_sourcemod_server_admin_group(instance)
    print(admins_groups)


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
