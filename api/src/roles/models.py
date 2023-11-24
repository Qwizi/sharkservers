import ormar
from typing import Optional, List
from src.db import BaseMeta, DateFieldsMixins
from src.scopes.models import Scope


class Role(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "roles"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=64, unique=True)
    color: str = ormar.String(max_length=256, default="#999999")
    scopes: Optional[List[Scope]] = ormar.ManyToMany(Scope)
    is_staff: Optional[bool] = ormar.Boolean(default=False)
