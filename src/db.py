import datetime
from sqlite3 import IntegrityError
from typing import Optional

import aioredis
import databases
import ormar
import sqlalchemy
from asyncpg import UniqueViolationError
from sqlite3 import IntegrityError as SQLIntegrityError
from fastapi import HTTPException
from fastapi_pagination import Params
from fastapi_pagination.ext.ormar import paginate
from ormar import Model
from starlette.requests import Request

from src.settings import get_settings

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


class BaseService:
    def __init__(self, model, not_found_exception, create_schema=None, update_schema=None):
        self.model = model
        self.not_found_exception = not_found_exception
        self.create_schema = Optional[Model]
        self.update_schema = None

    async def get_one(self, **kwargs) -> ormar.Model:
        try:
            related = kwargs.pop("related", None)
            if related:
                model = await self.model.objects.select_related(related).filter(
                    _exclude=False, **kwargs
                ).first()
            else:
                model = await self.model.objects.filter(
                    _exclude=False, **kwargs
                ).first()
            return model
        except ormar.NoMatch:
            raise self.not_found_exception

    async def get_all(self, params: Params = None, related=None):
        if params:
            return await paginate(self.model.objects, params)
        if related:
            return await self.model.objects.select_related(related).all()
        if related and params:
            return await paginate(self.model.objects.select_related(related), params)
        return await self.model.objects.all()

    async def delete(self, _id: int):
        _object = await self.get_one(id=_id)
        await _object.delete()
        return _object

    async def create(self, *args, **kwargs):
        async def route(schema: self.create_schema):  # type: ignore
            schema_dict = schema.dict()
            try:
                return await self.model.objects.create(**schema_dict)
            except (IntegrityError, SQLIntegrityError, UniqueViolationError):
                raise HTTPException(422, "Key already exists") from None

        return await route(*args, **kwargs)

    """
        async def update(self, _id: int, model: self.update_schema, **kwargs):  # type: ignore
        try:
            await self.model.objects.filter(_exclude=False, **kwargs).update(
                **model.dict(exclude_unset=True)
            )
        except (IntegrityError, SQLIntegrityError, UniqueViolationError):
            raise HTTPException(422, "Key already exists") from None
    """
