import ormar

from app.db import BaseMeta, DateFieldsMixins


class User(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=64, unique=True)
    email: str = ormar.String(max_length=255, unique=True)
    password: str = ormar.String(max_length=255)
    is_activated: bool = ormar.Boolean(default=False)
    is_superuser: bool = ormar.Boolean(default=False)
    avatar: str = ormar.String(max_length=255, default="/media/images/avatars/default_avatar.png")
