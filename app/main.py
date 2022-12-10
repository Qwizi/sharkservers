import logging
from logging.config import dictConfig
from typing import List

import aioredis
import uvicorn
from fastapi import FastAPI, Depends
from fastapi_events.dispatcher import dispatch
from fastapi_events.handlers.local import local_handler
from fastapi_events.middleware import EventHandlerASGIMiddleware
from pydantic import BaseModel
from starlette.requests import Request

from app.__version import VERSION
from app.auth.schemas import ActivateUserCode
from app.auth.utils import create_activate_code, activate_user
from app.db import database, create_redis_pool, get_redis
from app.logger import logger
from app.roles.utils import create_default_roles
from app.scopes.models import Scope
from app.scopes.utils import create_scopes
from app.settings import Settings, get_settings
from app.users.models import User
from fastapi_pagination import add_pagination
from fastapi_events.typing import Event
from app.users.schemas import UserEvents
# Routes
from app.users.views import router as users_router
from app.auth.views import router as auth_router
from app.scopes.views import router as scopes_router
from app.roles.views import router as roles_router

from app.users.handlers import (
    handle_user_register_event,
    create_activate_code_after_register
)


def create_app():
    _app = FastAPI(
        version=VERSION,
        debug=True
    )
    _app.add_middleware(EventHandlerASGIMiddleware, handlers=[local_handler])

    _app.state.database = database
    _app.include_router(users_router, prefix="/users", tags=["users"])
    _app.include_router(auth_router, prefix="/auth", tags=["auth"])
    _app.include_router(scopes_router, prefix="/scopes", tags=["scopes"])
    _app.include_router(roles_router, prefix="/roles", tags=["roles"])
    add_pagination(_app)

    @_app.on_event("startup")
    async def startup():
        logger.info("Application started")
        database_ = _app.state.database
        if not database_.is_connected:
            await database.connect()
        _app.state.redis = await create_redis_pool()
        await create_scopes()
        await create_default_roles()

    @_app.on_event("shutdown")
    async def shutdown():
        database_ = _app.state.database
        if database_.is_connected:
            await database_.disconnect()
        await app.state.redis.close()

    @_app.get("/")
    async def home():
        return {}

    return _app


app = create_app()
