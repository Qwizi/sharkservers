from contextlib import asynccontextmanager
import os
from fastapi import APIRouter, FastAPI
from .db import REDIS_URL, create_redis_pool, database
from fastapi_limiter import FastAPILimiter
from broadcaster import Broadcast

broadcast = Broadcast(REDIS_URL)

script_dir = os.path.dirname(__file__)
st_abs_file_path = os.path.join(script_dir, "../static/")
installed_file_path = os.path.join(script_dir, "installed")


def custom_generate_unique_id(route: APIRouter):
    return f"{route.tags[0]}-{route.name}"


async def init_limiter(_app: FastAPI):
    await FastAPILimiter.init(_app.state.redis)
    return _app


async def close_limiter(_app: FastAPI):
    await FastAPILimiter.close()
    return _app


async def connect_db(_app: FastAPI):
    _app.state.database = database
    database_ = _app.state.database
    if not database_.is_connected:
        await database.connect()
    _app.state.redis = await create_redis_pool()
    await FastAPILimiter.init(_app.state.redis)
    return _app


async def disconnect_db(_app: FastAPI):
    database_ = _app.state.database
    if database_.is_connected:
        await database_.disconnect()
    await _app.state.redis.close()


async def connect_broadcast(_app: FastAPI):
    _app.state.broadcast = broadcast
    await broadcast.connect()
    return _app


async def disconnect_broadcast(_app: FastAPI):
    broadcast_ = _app.state.broadcast
    await broadcast_.disconnect()


@asynccontextmanager
async def app_lifespan(_app: FastAPI):
    await connect_db(_app)
    await connect_broadcast(_app)
    await init_limiter(_app)
    yield
    await disconnect_db(_app)
    await disconnect_broadcast(_app)
    await close_limiter(_app)
