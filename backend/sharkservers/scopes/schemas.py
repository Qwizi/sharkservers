"""Schemas for scopes module."""
from __future__ import annotations

from pydantic import BaseModel
from uuidbase62 import UUIDBase62ModelMixin, con_uuidbase62

from sharkservers.scopes.models import Scope

scope_out = Scope.get_pydantic(exclude={"roles"})


class ScopeOut(UUIDBase62ModelMixin, scope_out):
    """ScopeOut schema."""

    id: con_uuidbase62(prefix="scope")


class CreateScopeSchema(BaseModel):
    """Create scope schema."""

    app_name: str
    value: str
    description: str
    protected: bool = True


class UpdateScopeSchema(BaseModel):
    """Update scope schema."""

    app_name: str | None
    value: str | None
    description: str | None
    protected: str | None
