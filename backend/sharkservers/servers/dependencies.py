"""Dependencies for the servers module."""
from fastapi import Depends
from ormar import Model
from uuidbase62 import UUIDBase62, get_validated_uuidbase62_by_model

from sharkservers.servers.schemas import ServerOut
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
    server_id: UUIDBase62 = Depends(
        get_validated_uuidbase62_by_model(ServerOut, "id", "server_id"),
    ),
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
    return await servers_service.get_one(id=server_id.uuid, related=["admin_role"])
