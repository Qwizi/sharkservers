from typing import Optional, List

import ormar

from app.db import BaseMeta
from app.scopes.models import Scope


class Role(ormar.Model):
    class Meta(BaseMeta):
        tablename = "roles"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=64, unique=True)
    color: str = ormar.String(max_length=256, default="#999999")
    scopes: Optional[List[Scope]] = ormar.ManyToMany(Scope)
    is_staff: Optional[bool] = ormar.Boolean(default=False)
