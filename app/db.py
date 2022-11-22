import databases
import sqlalchemy

from app.settings import get_settings

settings = get_settings()

DATABASE_URL = settings.get_database_url()

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)