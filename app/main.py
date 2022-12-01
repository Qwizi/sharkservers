from typing import List

from fastapi import FastAPI

from app.__version import VERSION
from app.db import database
from app.scopes.utils import create_scopes_for_application
from app.users.models import User
from app.users.views import router as users_router
from app.auth.views import router as auth_router
from fastapi_pagination import add_pagination

from app.utils import create_scopes


def create_app():
    _app = FastAPI(
        version=VERSION,
        debug=True
    )

    _app.state.database = database
    _app.include_router(users_router, prefix="/users", tags=["users"])
    _app.include_router(auth_router, prefix="/auth", tags=["auth"])
    add_pagination(_app)

    @_app.on_event("startup")
    async def startup():
        database_ = _app.state.database
        if not database_.is_connected:
            await database.connect()
        scopes = create_scopes(["users"])
        print(scopes)

    @_app.on_event("shutdown")
    async def shutdown():
        database_ = _app.state.database
        if database_.is_connected:
            await database_.disconnect()

    @_app.get("/")
    async def home():
        return {}

    return _app


app = create_app()
