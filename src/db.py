import datetime
from sqlite3 import IntegrityError as SQLIntegrityError

from redis import asyncio as aioredis
import databases
import ormar
import sqlalchemy
from asyncpg import UniqueViolationError
from fastapi import HTTPException
from fastapi_pagination import Params
from fastapi_pagination.ext.ormar import paginate
from psycopg2 import IntegrityError
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
    class Meta:
        model: ormar.Model = None
        not_found_exception: HTTPException = None

    async def get_one(self, **kwargs) -> ormar.Model:
        try:
            related = kwargs.pop("related", None)
            if related:
                model = (
                    await self.Meta.model.objects.select_related(related)
                    .filter(_exclude=False, **kwargs)
                    .first()
                )
            else:
                model = await self.Meta.model.objects.filter(
                    _exclude=False, **kwargs
                ).first()
            return model
        except ormar.NoMatch:
            raise self.Meta.not_found_exception

    async def get_all(
            self, params: Params = None, related=None, order_by=None, **kwargs
    ):
        """
        if params:
            if related:
                return await paginate(self.Meta.model.objects.select_related(related), params)
            else:
                return await paginate(self.Meta.model.objects, params)
        if related:
            return await self.Meta.model.objects.select_related(related).all()
        return await self.Meta.model.objects.all()
        :param params:
        :param related:
        :param kwargs:
        :return:
        """

        query = self.Meta.model.objects.filter(**kwargs)
        if related:
            query = query.select_related(related)
        if order_by:
            query = query.order_by(order_by)
        if params:
            query = await paginate(query, params)
        return query

    async def delete(self, _id: int):
        _object = await self.get_one(id=_id)
        await _object.delete()
        return _object

    async def create(self, *args, **kwargs):
        try:
            return await self.Meta.model.objects.create(**kwargs)
        except (IntegrityError, SQLIntegrityError, UniqueViolationError):
            raise HTTPException(status_code=422, detail="Key already exists")

    async def update(self, updated_data: dict, **kwargs):  # type: ignore
        try:
            related = kwargs.pop("related", None)
            await self.Meta.model.objects.filter(_exclude=False, **kwargs).update(
                **updated_data
            )
            return await self.get_one(**kwargs, related=related)
        except (IntegrityError, SQLIntegrityError, UniqueViolationError):
            raise HTTPException(422, "Key already exists")
