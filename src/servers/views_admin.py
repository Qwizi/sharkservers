from fastapi import APIRouter, Depends

from src.auth.dependencies import get_admin_user
from src.servers.schemas import ServerOut, CreateServerSchema
from src.servers.services import servers_service

router = APIRouter(dependencies=[Depends(get_admin_user)])


@router.post("", response_model=ServerOut)
async def admin_create_server(server_data: CreateServerSchema):
    """
    Create a new server
    :param server_data:
    :return:
    """
    return await servers_service.create(**server_data.dict())


@router.delete("/{server_id}")
async def admin_delete_server(server_id: int):
    """
    Delete a server
    :param server_id:
    :return:
    """
    return await servers_service.delete(server_id)
