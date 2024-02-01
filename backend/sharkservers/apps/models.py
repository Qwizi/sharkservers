# apps models
from typing import Optional

import ormar

from sharkservers.db import BaseMeta, DateFieldsMixins
from sharkservers.scopes.models import Scope
from sharkservers.users.models import User


class App(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "apps"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100)
    description: str = ormar.String(max_length=100)
    owner: User = ormar.ForeignKey(User)
    scopes: list[Scope] = ormar.ManyToMany(Scope, related_name="app_scopes")
    is_activated: bool = ormar.Boolean(default=True)
    client_id: Optional[str] = ormar.String(max_length=16, nullable=True)
    client_secret: Optional[str] = ormar.String(max_length=50, nullable=True)
    secret_key: Optional[str] = ormar.String(max_length=32, nullable=True)
