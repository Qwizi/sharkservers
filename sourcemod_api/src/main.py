
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from src.db import database
from src.admins.views.admins import router as admins_router
from src.admins.views.groups import router as groups_router
def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"

async def connect_db(_app: FastAPI):
    database_ = _app.state.database
    if not database_.is_connected:
        await database.connect()

async def disconnect_db(_app: FastAPI):
    database_ = _app.state.database
    if database_.is_connected:
        await database_.disconnect()

@asynccontextmanager
async def app_lifespan(_app: FastAPI):
    await connect_db(_app)
    yield
    await disconnect_db(_app)

def create_app() -> FastAPI:
    _app = FastAPI(
        name="FastApi Sourcemod Admin REST",
        version="0.0.1",
        debug=True,
        generate_unique_id_function=custom_generate_unique_id,
        lifespan=app_lifespan
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.state.database = database

    
    _app.include_router(admins_router, prefix="/v1/admins", tags=['adminss'])
    _app.include_router(groups_router, prefix="/v1/admins/groups", tags=["admins-groups"])

    return _app

app = create_app()