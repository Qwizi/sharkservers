import datetime

import databases
import ormar
import sqlalchemy

from app.settings import get_settings

settings = get_settings()

DATABASE_URL = settings.get_database_url()

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata


class DateFieldsMixins:
    created_date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    updated_date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
