"""Dependencies for the servers module."""
from fastapi import Depends
from ormar import Model

from sharkservers.servers.services import ServerService


async def get_servers_service() -> ServerService:
    """
    Retrieve the server service.

    Returns
    -------
        ServerService: The server service instance.
    """
    return ServerService()


async def get_valid_server(
    server_id: int,
    servers_service: ServerService = Depends(get_servers_service),
) -> Model:
    """
    Retrieve a valid server with the given server ID.

    Args:
    ----
        server_id (int): The ID of the server to retrieve.
        servers_service (ServerService): The server service dependency.

    Returns:
    -------
        Model: The retrieved server model.

    """
    return await servers_service.get_one(id=server_id, related=["admin_role"])
