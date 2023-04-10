import ormar
from ormar import post_save

from src.db import BaseMeta, DateFieldsMixins
from src.logger import logger
from src.players.models import Player, PlayerStats
from src.roles.dependencies import get_roles_service
from src.roles.enums import ProtectedDefaultRolesEnum
from src.scopes.dependencies import get_scopes_service


class Server(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "servers"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=64, unique=True)
    ip: str = ormar.String(max_length=64, unique=True)
    port: int = ormar.Integer()


class ServerPlayerStats(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "server_stats"

    id: int = ormar.Integer(primary_key=True)
    server: Server = ormar.ForeignKey(Server, related_name="server_stats")
    player: Player = ormar.ForeignKey(Player, related_name="player_stats")
    stats: list[PlayerStats] = ormar.ManyToMany(PlayerStats, related_name="stats")


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
