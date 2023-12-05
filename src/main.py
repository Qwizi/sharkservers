import os

import anyio
from aiocron import crontab
from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.middleware.gzip import GZipMiddleware
from fastapi_events.handlers.local import local_handler
from fastapi_events.middleware import EventHandlerASGIMiddleware
from fastapi_pagination import add_pagination
from jose import JWTError
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.staticfiles import StaticFiles

from src.__version import VERSION
from src.auth.dependencies import (
    get_access_token_service,
)
from src.auth.services.auth import AuthService
from src.auth.views import router as auth_router_v1
from src.chat.dependencies import get_chat_service
from src.chat.dependencies import ws_get_current_user
from src.chat.services import ChatService
from src.chat.views import router as chat_router
from src.forum.views import (
    router_v1 as forum_router,
    admin_router_v1 as admin_forum_router,
)
from src.players.views import router as steamprofile_router
from src.players.views_admin import router as admin_steamprofiles_router
from src.roles.views import router as roles_router
from src.roles.views_admin import router as admin_roles_router
from src.scopes.views import router as scopes_router
from src.scopes.views_admin import router as admin_scopes_router
from src.servers.views.servers import router as servers_router
from src.servers.views.admin.admins_groups import router as admin_admins_groups_router
from src.servers.views.admin.servers import router as admin_servers_router
from src.servers.views.admin.admins import router as admin_servers_admin_users_router
from src.settings import get_settings
from src.subscryptions.views import router as subscryptions_router

from src.users.models import User
# Routes
from src.users.views.users import router as users_router
from src.users.views.me import router as users_me_router
# Admin Routes
from src.users.views_admin import (
    router as admin_users_router,
)
from .auth.utils import now_datetime
from .chat.websocket import chatroom_ws_receiver, chatroom_ws_sender
from .forum.dependencies import (
    get_categories_service,
    get_threads_service,
    get_posts_service,
)
# import admin posts router
from .logger import logger
from .users.dependencies import get_users_service
from .utils import app_lifespan, custom_generate_unique_id
# Routers
from .views import router as root_router

script_dir = os.path.dirname(__file__)
st_abs_file_path = os.path.join(script_dir, "../static/")
installed_file_path = os.path.join(script_dir, "installed")


def init_routes(_app: FastAPI):
    # V1 routes
    _app.include_router(root_router, tags=["root"])
    _app.include_router(auth_router_v1, prefix="/v1/auth", tags=["auth"])
    _app.include_router(users_router, prefix="/v1/users", tags=["users"])
    _app.include_router(users_me_router, prefix="/v1/users/me", tags=["users-me"])
    _app.include_router(scopes_router, prefix="/v1/scopes", tags=["scopes"])
    _app.include_router(roles_router, prefix="/v1/roles", tags=["roles"])
    _app.include_router(steamprofile_router, prefix="/v1/players", tags=["players"])
    _app.include_router(forum_router)
    _app.include_router(servers_router, prefix="/v1/servers", tags=["servers"])
    _app.include_router(chat_router, prefix="/v1/chat", tags=["chat"])
    _app.include_router(
        subscryptions_router, prefix="/v1/subscryption", tags=["subscryption"]
    )

    # Admin routes
    _app.include_router(
        admin_users_router, prefix="/v1/admin/users", tags=["admin-users"]
    )
    _app.include_router(
        admin_roles_router, prefix="/v1/admin/roles", tags=["admin-roles"]
    )
    _app.include_router(
        admin_scopes_router, prefix="/v1/admin/scopes", tags=["admin-scopes"]
    )
    _app.include_router(
        admin_steamprofiles_router, prefix="/v1/admin/players", tags=["admin-players"]
    )
    _app.include_router(admin_forum_router)
    _app.include_router(
        admin_servers_router, prefix="/v1/admin/servers", tags=["admin-servers"]
    )
    _app.include_router(admin_admins_groups_router, prefix="/v1/admin/servers", tags=["admin-servers-admin-groups"])
    _app.include_router(admin_servers_admin_users_router, prefix="/v1/admin/servers", tags=["admin-servers-admins"])
    return _app


@crontab("* * * * *")
async def update_tables_counters():
    try:
        logger.info("Updating tables counters")
        categories_service = await get_categories_service()
        threads_service = await get_threads_service()
        posts_service = await get_posts_service()
        users_service = await get_users_service()
        await categories_service.sync_counters()
        await threads_service.sync_counters()
        await posts_service.sync_counters()
        await users_service.sync_counters(
            threads_service=threads_service, posts_service=posts_service
        )
        logger.info("Finished updating tables counters")
    except Exception as e:
        logger.error(e)


def add_middlewares(_app: FastAPI):
    @_app.middleware("http")
    async def update_user_last_online_time_middleware(request: Request, call_next):
        settings = get_settings()
        response = await call_next(request)
        if "Authorization" not in request.headers:
            return response
        try:
            access_token_service = await get_access_token_service(settings=settings)
            jwt_token = await AuthService.oauth2_scheme(request=request)
            token_data = access_token_service.decode_token(jwt_token)
            users_service = await get_users_service()
            user = await users_service.get_one(id=token_data.user_id)
            await user.update(last_online=now_datetime())
            return response
        except (JWTError, HTTPException):
            return response

    _app.add_middleware(GZipMiddleware)
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:3001" "https://api-sharkservers.qwizi.dev",
            "https://beta.sharkservers.pl",
            "https://api.sharkservers.pl",
            "https://api-beta.sharkservers.pl",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    event_handler_id: int = id(_app)
    _app.add_middleware(
        EventHandlerASGIMiddleware,
        handlers=[local_handler],
        middleware_id=event_handler_id,
    )
    return _app


def create_app():
    _app = FastAPI(
        name="Shark API",
        version=VERSION,
        debug=True,
        generate_unique_id_function=custom_generate_unique_id,
        lifespan=app_lifespan
    )
    _app = add_middlewares(_app)
    _app.mount("/static", StaticFiles(directory=st_abs_file_path), name="static")
    init_routes(_app)
    add_pagination(_app)

    @_app.websocket("/ws")
    async def websocket_endpoint(
            websocket: WebSocket,
            chat_service: ChatService = Depends(get_chat_service),
            author: User = Depends(ws_get_current_user),
    ):
        try:
            logger.info(_app.state.broadcast)
            await websocket.accept()

            async with anyio.create_task_group() as task_group:
                # run until first is complete
                async def run_chatroom_ws_receiver() -> None:
                    await chatroom_ws_receiver(
                        websocket=websocket, chat_service=chat_service, author=author
                    )
                    await task_group.cancel_scope.cancel()

                task_group.start_soon(run_chatroom_ws_receiver)
                await chatroom_ws_sender(
                    websocket, chat_service=chat_service, author=author
                )
        except WebSocketDisconnect:
            pass

    return _app


app = create_app()
