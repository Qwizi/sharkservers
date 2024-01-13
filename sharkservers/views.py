"""
Module containing the API routes for the SharkServers application.

Includes routes for installation, generating OpenAPI documentation,
and generating random data.

Routes:
- /install: POST route for installing the application.
- /generate-openapi: GET route for generating the OpenAPI documentation.
- /generate-random-data: GET route for generating random data for testing purposes.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends
from fastapi_events.dispatcher import dispatch

from sharkservers.auth.dependencies import get_auth_service
from sharkservers.forum.dependencies import (
    get_categories_service,
    get_posts_service,
    get_threads_service,
)
from sharkservers.roles.dependencies import get_roles_service
from sharkservers.scopes.dependencies import get_scopes_service
from sharkservers.servers.dependencies import get_servers_service
from sharkservers.services import MainService
from sharkservers.settings import Settings, get_settings
from sharkservers.utils import installed_file_path


from sharkservers.auth.schemas import RegisterUserSchema
from sharkservers.auth.services.auth import AuthService
from sharkservers.forum.services import CategoryService, PostService, ThreadService
from sharkservers.roles.services import RoleService
from sharkservers.scopes.services import ScopeService
from sharkservers.servers.services import ServerService

router = APIRouter()


@router.post("/install")
async def install(  # noqa: D417
    user_data: RegisterUserSchema,
    scopes_service: ScopeService = Depends(get_scopes_service),  # noqa: B008
    roles_service: RoleService = Depends(get_roles_service),  # noqa: B008
    auth_service: AuthService = Depends(get_auth_service),  # noqa: B008
    settings: Settings = Depends(get_settings), # noqa: B008
) -> dict:
    """
    Endpoint for installing the SharkServers application.

    Args:
    ----
    - user_data: User data for the admin user.
    - scopes_service: Service for managing scopes.
    - roles_service: Service for managing roles.
    - auth_service: Service for authentication.
    - settings: Application settings.

    Returns:
    -------
    - A dictionary with a "msg" key indicating the success of the installation.
    """
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
async def generate_openapi() -> dict[str, str]:
    """
    Endpoint for generating the OpenAPI documentation.

    Returns
    -------
    - A dictionary with a "msg" key indicating the success of the generation.
    """
    await MainService.generate_openapi_file()
    return {"msg": "Done"}


@router.get("/generate-random-data")
async def generate_random_data(  # noqa: PLR0913, D417
    auth_service: AuthService = Depends(get_auth_service),  # noqa: B008
    roles_service: RoleService = Depends(get_roles_service),  # noqa: B008
    categories_service: CategoryService = Depends(get_categories_service),  # noqa: B008
    threads_service: ThreadService = Depends(get_threads_service),  # noqa: B008
    posts_service: PostService = Depends(get_posts_service),  # noqa: B008
    servers_service: ServerService = Depends(get_servers_service),  # noqa: B008
) -> dict[str, str]:
    """
    Endpoint for generating random data for testing purposes.

    Args:
    ----
    - auth_service: Service for authentication.
    - roles_service: Service for managing roles.
    - categories_service: Service for managing categories.
    - threads_service: Service for managing threads.
    - posts_service: Service for managing posts.
    - servers_service: Service for managing servers.

    Returns:
    -------
    - A dictionary with a "msg" key indicating the success of the generation.
    """
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
