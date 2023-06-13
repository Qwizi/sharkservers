import datetime
import os

from fastapi import FastAPI, Depends, Security
from fastapi.routing import APIRoute
from fastapi_events.dispatcher import dispatch
from fastapi_events.handlers.local import local_handler
from fastapi_events.middleware import EventHandlerASGIMiddleware
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from src.__version import VERSION
from src.auth.dependencies import get_auth_service, get_application, get_ban_service
from src.auth.schemas import RegisterUserSchema
from src.auth.services import AuthService

# Events
from src.auth.views import router as auth_router_v1
from src.db import database, create_redis_pool
from src.forum.views import (
    router_v1 as forum_router,
    admin_router_v1 as admin_forum_router,
)
from src.players.views import router as steamprofile_router
from src.players.views_admin import router as admin_steamprofiles_router
from src.roles.dependencies import get_roles_service
from src.roles.services import RoleService
from src.roles.views import router as roles_router
from src.roles.views_admin import router as admin_roles_router
from src.scopes.dependencies import get_scopes_service
from src.scopes.services import ScopeService
from src.scopes.views import router as scopes_router
from src.scopes.views_admin import router as admin_scopes_router
from src.servers.views import router as servers_router
from src.servers.views_admin import router as admin_servers_router
from src.services import MainService
from src.chat.views import router as chat_router
from aiocron import crontab

# Routes
from src.users.views import router as users_router_v1

# Admin Routes
from src.users.views_admin import (
    router as admin_users_router,
    bans_router as admin_bans_router,
)
from .apps.models import App
from .forum.dependencies import get_categories_service, get_threads_service
from .forum.services import CategoryService, ThreadService

# import admin posts router


from .handlers import handle_all_events_and_debug_log, generate_random_data
from .auth.handlers import create_activate_code_after_register
from .logger import logger
from .users.dependencies import get_users_service
from .users.services import UserService
from .auth.handlers import create_activate_code_after_register

script_dir = os.path.dirname(__file__)
st_abs_file_path = os.path.join(script_dir, "../static/")
installed_file_path = os.path.join(script_dir, "installed")


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


async def connect_db(_app: FastAPI):
    database_ = _app.state.database
    if not database_.is_connected:
        await database.connect()
    _app.state.redis = await create_redis_pool()
    return _app


async def disconnect_db(_app: FastAPI):
    database_ = _app.state.database
    if database_.is_connected:
        await database_.disconnect()
    await app.state.redis.close()


def init_routes(_app: FastAPI):
    # V1 routes
    _app.include_router(auth_router_v1, prefix="/v1/auth", tags=["auth"])
    _app.include_router(users_router_v1, prefix="/v1/users", tags=["users"])
    _app.include_router(scopes_router, prefix="/v1/scopes", tags=["scopes"])
    _app.include_router(roles_router, prefix="/v1/roles", tags=["roles"])
    _app.include_router(steamprofile_router, prefix="/v1/players", tags=["players"])
    _app.include_router(forum_router)
    _app.include_router(servers_router, prefix="/v1/servers", tags=["servers"])
    _app.include_router(chat_router, prefix="/v1/chat", tags=["chat"])

    # Admin routes
    _app.include_router(admin_users_router, prefix="/admin/users", tags=["admin-users"])
    _app.include_router(admin_bans_router, prefix="/v1/admin/bans", tags=["admin-bans"])
    _app.include_router(admin_roles_router, prefix="/admin/roles", tags=["admin-roles"])
    _app.include_router(
        admin_scopes_router, prefix="/admin/scopes", tags=["admin-scopes"]
    )
    _app.include_router(
        admin_steamprofiles_router, prefix="/admin/players", tags=["admin-players"]
    )
    _app.include_router(admin_forum_router)
    _app.include_router(
        admin_servers_router, prefix="/admin/servers", tags=["admin-servers"]
    )
    return _app


async def unban_users_cron():
    # This is an async cron job that runs every minute
    logger.info("Cron job ran")

    users_service = await get_users_service()
    roles_service = await get_roles_service()
    scopes_service = await get_scopes_service()
    auth_service = await get_auth_service(
        users_service=users_service,
        roles_service=roles_service,
        scopes_service=scopes_service,
    )
    ban_service = await get_ban_service(
        auth_service=auth_service, roles_service=roles_service
    )
    active_bans = await ban_service.Meta.model.objects.filter(
        ban_time__lte=datetime.datetime.utcnow()
    ).all()

    now = datetime.datetime.utcnow()

    for ban in active_bans:
        logger.info(ban.ban_time.date())
        if ban.ban_time < now:
            await ban_service.unban_user(ban.user)

    logger.info(active_bans)


@crontab("* * * * *")
async def my_cron_job():
    # This function calls the async cron job function
    await unban_users_cron()


def create_app():
    _app = FastAPI(
        name="Shark API",
        version=VERSION,
        debug=True,
        generate_unique_id_function=custom_generate_unique_id,
    )
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.add_middleware(EventHandlerASGIMiddleware, handlers=[local_handler])
    _app.mount("/static", StaticFiles(directory=st_abs_file_path), name="static")
    _app.state.database = database
    init_routes(_app)
    add_pagination(_app)

    @_app.on_event("startup")
    async def startup():
        await connect_db(_app)

    @_app.on_event("shutdown")
    async def shutdown():
        await disconnect_db(_app)

    @_app.post("/install", tags=["root"])
    async def install(
            user_data: RegisterUserSchema,
            scopes_service: ScopeService = Depends(get_scopes_service),
            roles_service: RoleService = Depends(get_roles_service),
            auth_service: AuthService = Depends(get_auth_service),
    ):
        await MainService.install(
            file_path=installed_file_path,
            admin_user_data=user_data,
            scopes_service=scopes_service,
            roles_service=roles_service,
            auth_service=auth_service,
        )
        return {"msg": "Successfully installed"}

    @_app.get("/generate-openapi", tags=["root"])
    async def generate_openapi():
        await MainService.generate_openapi_file()
        return {"msg": "Done"}

    @_app.get("/generate-random-data", tags=["root"])
    async def generate_random_data(
            auth_service: AuthService = Depends(get_auth_service),
            roles_service: RoleService = Depends(get_roles_service),
            categories_service: CategoryService = Depends(get_categories_service),
            threads_service: ThreadService = Depends(get_threads_service),
    ):
        dispatch(
            event_name="GENERATE_RANDOM_DATA",
            payload={
                "auth_service": auth_service,
                "roles_service": roles_service,
                "categories_service": categories_service,
                "threads_service": threads_service,
            },
        )
        return {"msg": "Done"}

    @_app.get("/protected", tags=["root"])
    async def protected_route(
            app: App = Security(get_application, scopes=["users:create"]),
    ):
        return {"msg": "You are authenticated!"}

    return _app


app = create_app()
