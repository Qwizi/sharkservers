# chat models
import ormar

from sharkservers.db import BaseMeta, DateFieldsMixins
from sharkservers.users.models import User


class Chat(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "chats"

    id: int = ormar.Integer(primary_key=True)
    author: User = ormar.ForeignKey(User)
    message: str = ormar.String(max_length=500)
