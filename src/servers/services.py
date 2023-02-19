from fastapi_pagination import Params

from src.db import BaseService
from src.servers.exceptions import server_not_found_exception
from src.servers.models import Server
from steam import game_servers as gs

from src.servers.schemas import ServerStatusSchema


class ServerService(BaseService):
    async def get_status(self):
        servers_with_status = []
        servers_from_db = await self.model.objects.all()
        for server in servers_from_db:
            try:
                server_status = gs.a2s_info((server.ip, server.port))
                name = server_status.get("name", "invalid name")
                players = server_status.get("players", 0)
                max_players = server_status.get("max_players", 0)
                map = server_status.get("map", "invalid_map")
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
            except ConnectionRefusedError as e:
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
                    )
                )

        return servers_with_status


servers_service = ServerService(
    model=Server, not_found_exception=server_not_found_exception
)