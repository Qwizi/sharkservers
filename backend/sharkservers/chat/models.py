# chat models
import uuid
import ormar

from sharkservers.db import BaseMeta, DateFieldsMixins
from sharkservers.users.models import User


class Chat(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "chats"

    id: str = ormar.UUID(primary_key=True, default=uuid.uuid4)
    author: User = ormar.ForeignKey(User)
    message: str = ormar.String(max_length=500)
