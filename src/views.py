from fastapi import APIRouter, Depends
from src.auth.dependencies import get_auth_service

from src.auth.schemas import RegisterUserSchema
from src.auth.services.auth import AuthService
from src.forum.dependencies import (
    get_categories_service,
    get_posts_service,
    get_threads_service,
)
from src.forum.services import CategoryService, PostService, ThreadService
from src.roles.dependencies import get_roles_service
from src.roles.services import RoleService
from src.scopes.dependencies import get_scopes_service
from src.scopes.services import ScopeService
from src.servers.dependencies import get_servers_service
from src.servers.services import ServerService
from src.services import MainService
from src.settings import Settings, get_settings
from src.utils import installed_file_path
from fastapi_events.dispatcher import dispatch

router = APIRouter()


@router.post("/install")
async def install(
    user_data: RegisterUserSchema,
    scopes_service: ScopeService = Depends(get_scopes_service),
    roles_service: RoleService = Depends(get_roles_service),
    auth_service: AuthService = Depends(get_auth_service),
    settings: Settings = Depends(get_settings),
):
    await MainService.install(
        file_path=installed_file_path,
        admin_user_data=user_data,
        scopes_service=scopes_service,
        roles_service=roles_service,
        auth_service=auth_service,
        settings=settings,
    )
    return {"msg": "Successfully installed"}


@router.get("/generate-openapi")
async def generate_openapi():
    await MainService.generate_openapi_file()
    return {"msg": "Done"}


@router.get("/generate-random-data")
async def generate_random_data(
    auth_service: AuthService = Depends(get_auth_service),
    roles_service: RoleService = Depends(get_roles_service),
    categories_service: CategoryService = Depends(get_categories_service),
    threads_service: ThreadService = Depends(get_threads_service),
    posts_service: PostService = Depends(get_posts_service),
    servers_service: ServerService = Depends(get_servers_service),
):
    dispatch(
        event_name="GENERATE_RANDOM_DATA",
        payload={
            "auth_service": auth_service,
            "roles_service": roles_service,
            "categories_service": categories_service,
            "threads_service": threads_service,
            "posts_service": posts_service,
            "servers_service": servers_service,
        },
    )
    return {"msg": "Done"}
