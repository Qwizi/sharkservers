import datetime

import aioredis
import databases
import ormar
import sqlalchemy
from starlette.requests import Request

from shark_api.settings import get_settings

settings = get_settings()

DATABASE_URL = settings.get_database_url()
REDIS_URL = settings.get_redis_url()
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


async def create_redis_pool():
    redis = aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    return redis


async def get_redis(request: Request):
    return request.app.state.redis


class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata


class DateFieldsMixins:
    created_date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    updated_date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
