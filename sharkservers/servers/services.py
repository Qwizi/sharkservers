"""Services for servers app."""
from __future__ import annotations

from steam import game_servers as gs

from sharkservers.db import BaseService
from sharkservers.servers.exceptions import (
    server_not_found_exception,
)
from sharkservers.servers.models import Server
from sharkservers.servers.schemas import ServerStatusSchema


class ServerService(BaseService):
    """
    Service class for managing server operations.

    Methods
    -------
        get_status(): Retrieves the status of all servers.

    """

    class Meta:
        """Metadata for the service."""

        model = Server
        not_found_exception = server_not_found_exception

    async def get_status(self) -> list[ServerStatusSchema]:
        """
        Retrieve the status of all servers.

        Returns
        -------
            list: A list of server status objects.
        """
        servers_with_status: list[ServerStatusSchema] = []
        servers_from_db = await self.Meta.model.objects.all()
        try:
            for server in servers_from_db:
                server_status = gs.a2s_info((server.ip, server.port))
                name = server_status.get("name", "invalid name")
                players = server_status.get("players", 0)
                max_players = server_status.get("max_players", 0)
                map = server_status.get("map", "invalid_map")  # noqa: A001
                server_status_schema = ServerStatusSchema(
                    id=server.id,
                    name=name,
                    ip=server.ip,
                    port=server.port,
                    players=players,
                    max_players=max_players,
                    map=map,
                    game="tf2",
                )
                servers_with_status.append(server_status_schema)
        except ConnectionRefusedError:
            servers_with_status.append(
                ServerStatusSchema(
                    id=server.id,
                    name=server.name,
                    ip=server.ip,
                    port=server.port,
                    players=0,
                    max_players=0,
                    map="invalid_map",
                    game="tf2",
                ),
            )

        return servers_with_status
