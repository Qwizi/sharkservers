from fastapi import APIRouter, Depends

from src.auth.dependencies import get_admin_user
from src.servers.dependencies import get_servers_service
from src.servers.schemas import ServerOut, CreateServerSchema
from src.servers.services import ServerService

router = APIRouter(dependencies=[Depends(get_admin_user)])


@router.post("", response_model=ServerOut)
async def admin_create_server(
    server_data: CreateServerSchema,
    servers_service: ServerService = Depends(get_servers_service),
):
    """
    Create a new server
    :param servers_service:
    :param server_data:
    :return:
    """
    return await servers_service.create(**server_data.dict())


@router.delete("/{server_id}")
async def admin_delete_server(
    server_id: int,
    servers_service: ServerService = Depends(get_servers_service),
):
    """
    Delete a server
    :param servers_service:
    :param server_id:
    :return:
    """
    return await servers_service.delete(server_id)
