import json
import os
from pathlib import Path

import httpx
from fastapi import FastAPI, Header, Depends, HTTPException
from fastapi.routing import APIRoute
from fastapi_events.dispatcher import dispatch
from fastapi_events.handlers.local import local_handler
from fastapi_events.middleware import EventHandlerASGIMiddleware
from fastapi_mail import MessageSchema, MessageType
from pydantic import EmailStr
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from src.__version import VERSION
from src.auth.schemas import RegisterUserSchema
from src.auth.utils import create_admin_user
from src.db import database, create_redis_pool
from src.forum.models import Category
from src.logger import logger
from src.roles.utils import create_default_roles
from src.scopes.utils import create_scopes
from fastapi_pagination import add_pagination

from src.settings import get_settings

# Routes
from src.users.views import router as users_router
from src.auth.views import router as auth_router
from src.scopes.views import router as scopes_router
from src.roles.views import router as roles_router
from src.players.views import router as steamprofile_router
from src.forum.views.categories import router as forum_categories_router
from src.forum.views.threads import router as forum_threads_router
from src.forum.views.posts import router as forum_posts_router
from src.servers.views import router as servers_router

# Admin Routes
from src.users.views_admin import router as admin_users_router
from src.roles.views_admin import router as admin_roles_router
from src.scopes.views_admin import router as admin_scopes_router
from src.players.views_admin import router as admin_steamprofiles_router
from src.forum.views.admin.categories import router as admin_forum_categories_router
from src.forum.views.admin.threads import router as admin_forum_threads_router
from src.servers.views_admin import router as admin_servers_router

# import admin posts router
from src.forum.views.admin.posts import router as admin_forum_posts_router

# Events
from src.auth.handlers import create_activate_code_after_register
from src.players.handlers import create_player
from .enums import MainEventEnum

from .handlers import handle_all_events_and_debug_log, handle_install_event
from .scopes.services import scopes_service
from .services import email_service

script_dir = os.path.dirname(__file__)
st_abs_file_path = os.path.join(script_dir, "../static/")
installed_file_path = os.path.join(script_dir, "installed")


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


def create_app():
    _app = FastAPI(
        name="Shark API",
        version=VERSION,
        debug=True,
        generate_unique_id_function=custom_generate_unique_id,
    )
    _app.add_middleware(EventHandlerASGIMiddleware, handlers=[local_handler])

    _app.mount("/static", StaticFiles(directory=st_abs_file_path), name="static")
    _app.state.database = database
    _app.include_router(auth_router, prefix="/auth", tags=["auth"])
    _app.include_router(users_router, prefix="/users", tags=["users"])
    _app.include_router(scopes_router, prefix="/scopes", tags=["scopes"])
    _app.include_router(roles_router, prefix="/roles", tags=["roles"])
    _app.include_router(steamprofile_router, prefix="/players", tags=["players"])
    _app.include_router(
        forum_categories_router, prefix="/forum/categories", tags=["forum-categories"]
    )
    _app.include_router(
        forum_threads_router, prefix="/forum/threads", tags=["forum-threads"]
    )
    _app.include_router(forum_posts_router, prefix="/forum/posts", tags=["forum-posts"])
    _app.include_router(servers_router, prefix="/servers", tags=["servers"])

    # Admin routes
    _app.include_router(admin_users_router, prefix="/admin/users", tags=["admin-users"])
    _app.include_router(admin_roles_router, prefix="/admin/roles", tags=["admin-roles"])
    _app.include_router(
        admin_scopes_router, prefix="/admin/scopes", tags=["admin-scopes"]
    )
    _app.include_router(
        admin_steamprofiles_router, prefix="/admin/players", tags=["admin-players"]
    )
    _app.include_router(
        admin_forum_categories_router,
        prefix="/admin/forum/categories",
        tags=["admin-forum-categories"],
    )
    _app.include_router(
        admin_forum_threads_router,
        prefix="/admin/forum/threads",
        tags=["admin-forum-threads"],
    )
    _app.include_router(
        admin_servers_router, prefix="/admin/servers", tags=["admin-servers"]
    )
    # include admin forum posts router
    _app.include_router(
        admin_forum_posts_router,
        prefix="/admin/forum/posts",
        tags=["admin-forum-posts"],
    )
    add_pagination(_app)

    @_app.on_event("startup")
    async def startup():
        logger.info("Application started")
        database_ = _app.state.database
        if not database_.is_connected:
            await database.connect()
        _app.state.redis = await create_redis_pool()

    @_app.on_event("shutdown")
    async def shutdown():
        database_ = _app.state.database
        if database_.is_connected:
            await database_.disconnect()
        await app.state.redis.close()

    @_app.get("/", tags=["root"])
    async def home(settings=Depends(get_settings)):

        return {}

    @_app.get("/images", tags=["root"])
    async def get_images():
        images_list = []
        for filename in os.listdir(st_abs_file_path + "images"):
            images_list.append(
                {"name": filename.split(".")[0], "path": f"/static/images/{filename}"}
            )
        return images_list

    @_app.post("/install", tags=["root"])
    async def install(user_data: RegisterUserSchema):
        logger.info("#0 - Install started")
        if os.path.exists(installed_file_path):
            raise HTTPException(detail="Its already installed", status_code=400)
        await scopes_service.create_default_scopes(
            applications=[
                "users",
                "roles",
                "scopes",
                "players",
                "categories",
                "tags",
                "threads",
                "posts",
            ],
            additional=[
                ("users", "me", "Get my profile"),
                ("users", "me:username", "Update my username"),
                ("users", "me:password", "Update my password"),
                ("users", "me:display-role", "Update my display role"),
                ("threads", "open", "Open a thread"),
                ("threads", "close", "Close a thread"),
            ],
        )
        logger.info("#1 - Created scopes")
        await create_default_roles()
        logger.info("#2 - Created roles")
        await create_admin_user(user_data)
        logger.info("#3 - Created admin user")
        install_finish_file = open(installed_file_path, "w+")
        logger.info("#4 - Created installed file")
        dispatch(event_name=MainEventEnum.INSTALL)
        return {"msg": "Successfully installed"}

    @_app.get("/generate-openapi", tags=["root"])
    async def generate_openapi():
        url = "http://localhost/openapi.json"
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
            with open("openapi.json", "wb") as f:
                f.write(r.content)
            file_path = Path("./openapi.json")
            openapi_content = json.loads(file_path.read_text())

            for path_data in openapi_content["paths"].values():
                for operation in path_data.values():
                    tag = operation["tags"][0]
                    operation_id = operation["operationId"]
                    to_remove = f"{tag}-"
                    new_operation_id = operation_id[len(to_remove) :]
                    print(operation_id)
                    operation["operationId"] = new_operation_id
                    print(new_operation_id)
            file_path.write_text(json.dumps(openapi_content))
        return {"msg": "Done"}

    return _app


app = create_app()
