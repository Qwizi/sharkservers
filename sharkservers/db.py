"""
Module contains database-related functionality for the SharkServers API.

It defines the database connection, models, and base service class.
"""  # noqa: EXE002

import datetime
from sqlite3 import IntegrityError as SQLIntegrityError

import databases
import ormar
import sqlalchemy
from asyncpg import UniqueViolationError
from fakeredis import aioredis as fake_aioredis
from fastapi import HTTPException
from fastapi_pagination import Params
from fastapi_pagination.ext.ormar import paginate
from psycopg2 import IntegrityError
from redis import asyncio as aioredis
from starlette.requests import Request

from sharkservers.auth.utils import now_datetime
from sharkservers.settings import get_settings

settings = get_settings()

DATABASE_URL = settings.get_database_url()
REDIS_URL = settings.get_redis_url()
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


async def create_redis_pool() -> aioredis.Redis:
    """
    Create a Redis connection pool.

    Returns
    -------
        aioredis.Redis: The Redis connection pool.
    """
    if settings.TESTING:
        return await fake_aioredis.FakeRedis()
    return aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)


async def get_redis(request: Request) -> aioredis.Redis:
    """
    Get the Redis connection from the request.

    Args:
    ----
        request (Request): The incoming request.

    Returns:
    -------
        aioredis.Redis: The Redis connection.
    """
    return request.app.state.redis


class BaseMeta(ormar.ModelMeta):
    """
    Meta class for the BaseMeta class.

    This class defines the metadata and database attributes for ormar models.
    """

    database = database
    metadata = metadata


class DateFieldsMixins:
    """Mixin class that provides date fields for created_at and updated_at."""

    created_at: datetime.datetime = ormar.DateTime(
        default=now_datetime().replace(tzinfo=None),
        timezone=False,
    )
    updated_at: datetime.datetime = ormar.DateTime(
        default=now_datetime().replace(tzinfo=None),
        timezone=False,
    )


class BaseService:
    class Meta:
        model: ormar.Model = None
        not_found_exception: HTTPException = None

    async def get_one(self, **kwargs) -> ormar.Model:
        """
        Get a single model instance based on the provided filters.

        Args:
        ----
            **kwargs: The filters to apply.

        Returns:
        -------
            ormar.Model: The retrieved model instance.

        Raises:
        ------
            HTTPException: If no matching model instance is found.
        """
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
                    _exclude=False,
                    **kwargs,
                ).first()
            return model
        except ormar.NoMatch as err:
            raise self.Meta.not_found_exception from err

    async def get_all(
        self,
        params: Params = None,
        related=None,
        order_by=None,
        **kwargs,
    ):
        """
        Get all model instances based on the provided filters.

        Args:
        ----
            params (Params, optional): The pagination parameters.
            related (str, optional): The related model to include.
            order_by (str, optional): The field to order the results by.
            **kwargs: The filters to apply.

        Returns:
        -------
            QuerySet: The retrieved model instances.
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
        """
        Delete a model instance by its ID.

        Args:
        ----
            _id (int): The ID of the model instance to delete.

        Returns:
        -------
            ormar.Model: The deleted model instance.

        Raises:
        ------
            HTTPException: If no matching model instance is found.
        """
        _object = await self.get_one(id=_id)
        await _object.delete()
        return _object

    async def create(self, *args, **kwargs):
        """
        Create a new model instance.

        Args:
        ----
            *args: The positional arguments.
            **kwargs: The keyword arguments.

        Returns:
        -------
            ormar.Model: The created model instance.

        Raises:
        ------
            HTTPException: If a unique constraint is violated.
        """
        try:
            return await self.Meta.model.objects.create(**kwargs)
        except (IntegrityError, SQLIntegrityError, UniqueViolationError) as err:
            raise HTTPException(status_code=422, detail="Key already exists") from err

    async def update(self, updated_data: dict, **kwargs) -> ormar.Model:
        """
        Update a model instance.

        Args:
        ----
            updated_data (dict): The updated data.
            **kwargs: The filters to apply.

        Returns:
        -------
            ormar.Model: The updated model instance.

        Raises:
        ------
            HTTPException: If a unique constraint is violated.
        """
        try:
            related = kwargs.pop("related", None)
            await self.Meta.model.objects.filter(_exclude=False, **kwargs).update(
                **updated_data,
            )
            return await self.get_one(**kwargs, related=related)
        except (IntegrityError, SQLIntegrityError, UniqueViolationError) as err:
            raise HTTPException(422, "Key already exists") from err
