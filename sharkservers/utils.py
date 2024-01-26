"""
Utility functions and context managers used in the Sharkservers API.

Functions:
- custom_generate_unique_id: Generates a unique ID based on the route's tags and name.
- init_limiter: Initializes the rate limiter for the FastAPI application.
- close_limiter: Closes the rate limiter for the FastAPI application.
# - connect_db: Connects to the database and initializes the Redis connection and rate limiter.
- disconnect_db: Disconnects from the database and closes the Redis connection.
- connect_broadcast: Connects to the broadcast service.
- disconnect_broadcast: Disconnects from the broadcast service.

Context Managers:
- app_lifespan: Manages the lifespan of the FastAPI application.
"""
import os
from contextlib import asynccontextmanager
from typing import AsyncIterator

from broadcaster import Broadcast
from fastapi import APIRouter, FastAPI
from fastapi_limiter import FastAPILimiter

from .db import REDIS_URL, create_redis_pool, database

broadcast = Broadcast(REDIS_URL)

script_dir = os.path.dirname(__file__)  # noqa: PTH120
st_abs_file_path = os.path.join(script_dir, "../static/")  # noqa: PTH118
installed_file_path = os.path.join(script_dir, "installed")  # noqa: PTH118


def custom_generate_unique_id(route: APIRouter) -> str:
    """
    Generate a unique ID based on the route's tags and name.

    Args:
    ----
    route (APIRouter): The route for which to generate the unique ID.

    Returns:
    -------
        str: The generated unique ID.
    """
    return f"{route.tags[0]}-{route.name}"


async def init_limiter(_app: FastAPI) -> FastAPI:
    """
    Initialize the rate limiter for the FastAPI application.

    Args:
    ----
        _app (FastAPI): The FastAPI application.

    Returns:
    -------
        FastAPI: The updated FastAPI application.
    """
    await FastAPILimiter.init(_app.state.redis)
    return _app


async def close_limiter(_app: FastAPI) -> FastAPI:
    """
    Close the rate limiter for the FastAPI application.

    Args:
    ----
        _app (FastAPI): The FastAPI application.

    Returns:
    -------
        FastAPI: The updated FastAPI application.
    """
    await FastAPILimiter.close()
    return _app


async def connect_db(_app: FastAPI) -> FastAPI:
    """
    Connect to the database and initializes the Redis connection and rate limiter.

    Args:
    ----
        _app (FastAPI): The FastAPI application.

    Returns:
    -------
        FastAPI: The updated FastAPI application.
    """
    _app.state.database = database
    database_ = _app.state.database
    if not database_.is_connected:
        await database.connect()
    _app.state.redis = await create_redis_pool()
    await FastAPILimiter.init(_app.state.redis)
    return _app


async def disconnect_db(_app: FastAPI) -> None:
    """
    Disconnect from the database and closes the Redis connection.

    Args:
    ----
        _app (FastAPI): The FastAPI application.
    """
    database_ = _app.state.database
    if database_.is_connected:
        await database_.disconnect()
    await _app.state.redis.close()


async def connect_broadcast(_app: FastAPI) -> FastAPI:
    """
    Connect to the broadcast service.

    Args:
    ----
        _app (FastAPI): The FastAPI application.

    Returns:
    -------
        FastAPI: The updated FastAPI application.
    """
    _app.state.broadcast = broadcast
    await broadcast.connect()
    return _app


async def disconnect_broadcast(_app: FastAPI) -> None:
    """
    Disconnect from the broadcast service.

    Args:
    ----
        _app (FastAPI): The FastAPI application.
    """
    broadcast_ = _app.state.broadcast
    await broadcast_.disconnect()


@asynccontextmanager
async def app_lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """
    Manage the lifespan of the FastAPI application.

    Args:
    ----
        _app (FastAPI): The FastAPI application.

    Yields:
    ------
        None
    """
    await connect_db(_app)
    await connect_broadcast(_app)
    await init_limiter(_app)
    yield
    await disconnect_db(_app)
    await disconnect_broadcast(_app)
    await close_limiter(_app)
