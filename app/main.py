import os

import httpx
from fastapi import FastAPI, Header, Depends, HTTPException
from fastapi_events.handlers.local import local_handler
from fastapi_events.middleware import EventHandlerASGIMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from app.__version import VERSION
from app.auth.schemas import RegisterUserSchema
from app.auth.utils import create_admin_user
from app.db import database, create_redis_pool
from app.forum.models import Category
from app.logger import logger
from app.roles.utils import create_default_roles
from app.scopes.utils import create_scopes
from fastapi_pagination import add_pagination

from app.settings import get_settings

# Routes
from app.users.views import router as users_router
from app.auth.views import router as auth_router
from app.scopes.views import router as scopes_router
from app.roles.views import router as roles_router
from app.steamprofile.views import router as steamprofile_router
from app.forum.views_categories import router as forum_categories_router
from app.forum.views_tags import router as forum_tags_router
from app.forum.views_threads import router as forum_threads_router
from app.forum.views_posts import router as forum_posts_router

# Admin Routes
from app.users.views_admin import router as admin_users_router
from app.roles.views_admin import router as admin_roles_router
from app.scopes.views_admin import router as admin_scopes_router
from app.steamprofile.views_admin import router as admin_steamprofiles_router

# Events
from app.auth.handlers import (
    create_activate_code_after_register
)

from .handlers import handle_all_events_and_debug_log

script_dir = os.path.dirname(__file__)
st_abs_file_path = os.path.join(script_dir, "static/")
installed_file_path = os.path.join(script_dir, "installed")


def create_app():
    _app = FastAPI(
        name="Shark API",
        version=VERSION,
        debug=True
    )
    _app.add_middleware(EventHandlerASGIMiddleware, handlers=[local_handler])

    _app.mount("/static", StaticFiles(directory=st_abs_file_path), name="static")
    _app.state.database = database
    _app.include_router(auth_router, prefix="/auth", tags=["auth"])
    _app.include_router(users_router, prefix="/users", tags=["users"])
    _app.include_router(scopes_router, prefix="/scopes", tags=["scopes"])
    _app.include_router(roles_router, prefix="/roles", tags=["roles"])
    _app.include_router(steamprofile_router, prefix="/players", tags=["players"])
    _app.include_router(forum_categories_router, prefix="/forum/categories", tags=["forum-categories"])
    _app.include_router(forum_tags_router, prefix="/forum/tags", tags=["forum-tags"])
    _app.include_router(forum_threads_router, prefix="/forum/threads", tags=["forum-threads"])
    _app.include_router(forum_posts_router, prefix="/forum/posts", tags=["forum-posts"])

    # Admin routes
    _app.include_router(admin_users_router, prefix="/admin/users", tags=["admin-users"])
    _app.include_router(admin_roles_router, prefix="/admin/roles", tags=["admin-roles"])
    _app.include_router(admin_scopes_router, prefix="/admin/scopes", tags=["admin-scopes"])
    _app.include_router(admin_steamprofiles_router, prefix="/admin/players", tags=["admin-players"])

    add_pagination(_app)

    @_app.on_event("startup")
    async def startup():
        logger.info("Application started")
        database_ = _app.state.database
        if not database_.is_connected:
            await database.connect()
        _app.state.redis = await create_redis_pool()
        category, _created = await Category.objects.get_or_create(id=1, _defaults={
            "name": "Home"
        })

    @_app.on_event("shutdown")
    async def shutdown():
        database_ = _app.state.database
        if database_.is_connected:
            await database_.disconnect()
        await app.state.redis.close()

    @_app.get("/")
    async def home(settings=Depends(get_settings)):
        print(settings.STEAM_API_KEY)
        return {}

    @_app.get("/images")
    async def get_images():
        images_list = []
        for filename in os.listdir(st_abs_file_path + "images"):
            images_list.append({
                "name": filename.split(".")[0],
                "path": f"/static/images/{filename}"
            })
        return images_list

    @_app.post("/install")
    async def install(user_data: RegisterUserSchema):
        logger.info("#0 - Install started")
        if os.path.exists(installed_file_path):
            raise HTTPException(detail="Its already installed", status_code=400)
        await create_scopes()
        logger.info("#1 - Created scopes")
        await create_default_roles()
        logger.info("#2 - Created roles")
        await create_admin_user(user_data)
        logger.info("#3 - Created admin user")
        install_finish_file = open(installed_file_path, "w+")
        logger.info("#4 - Created installed file")
        return {"msg": "Successfully installed"}

    return _app


app = create_app()
