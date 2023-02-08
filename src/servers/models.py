import ormar

from src.db import BaseMeta, DateFieldsMixins


class Server(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "servers"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=64, unique=True)
    ip: str = ormar.String(max_length=64, unique=True)
    port: int = ormar.Integer()
