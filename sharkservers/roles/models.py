"""Roles models."""
from __future__ import annotations

import ormar

from sharkservers.db import BaseMeta, DateFieldsMixins
from sharkservers.scopes.models import Scope


class Role(ormar.Model, DateFieldsMixins):
    """
    Represent a role in the system.

    Attributes
    ----------
        id (int): The unique identifier of the role.
        tag (str, optional): The tag associated with the role.
        name (str, optional): The name of the role.
        color (str, optional): The color associated with the role.
        scopes (List[Scope], optional): The list of scopes associated with the role.
        is_staff (bool, optional): Indicates if the role is a staff role.
    """

    class Meta(BaseMeta):
        """Role metadata."""

        tablename = "roles"

    id: int = ormar.Integer(primary_key=True)
    tag: str | None = ormar.String(max_length=64, unique=True)
    name: str | None = ormar.String(max_length=64)
    color: str | None = ormar.String(max_length=256, default="#999999")
    scopes: list[Scope] | None = ormar.ManyToMany(Scope)
    is_staff: bool | None = ormar.Boolean(default=False)
