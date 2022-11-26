from typing import List

from fastapi import FastAPI

from app.__version import VERSION
from app.db import database
from app.users.models import User


def create_app():
    _app = FastAPI(
        version=VERSION,
        debug=True
    )

    _app.state.database = database

    @_app.on_event("startup")
    async def startup():
        database_ = _app.state.database
        if not database_.is_connected:
            await database.connect()

    @_app.on_event("shutdown")
    async def shutdown():
        database_ = _app.state.database
        if database_.is_connected:
            await database_.disconnect()

    @_app.get("/")
    async def home(response_model=List[User]):
        return {}

    return _app


app = create_app()
