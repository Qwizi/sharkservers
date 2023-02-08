from src.db import BaseService
from src.servers.exceptions import server_not_found_exception
from src.servers.models import Server


class ServerService(BaseService):
    pass


servers_service = ServerService(model=Server, not_found_exception=server_not_found_exception)
