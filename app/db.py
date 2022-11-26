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


class CreatedUpdatedModel(ormar.Model):
    created_at = ormar.DateTime(default=datetime.datetime.utcnow())
    updated_at = ormar.DateTime(default=datetime.datetime.utcnow())
