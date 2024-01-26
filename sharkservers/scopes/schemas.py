"""Schemas for scopes module."""
from __future__ import annotations

from pydantic import BaseModel

from sharkservers.scopes.models import Scope

ScopeOut = Scope.get_pydantic(exclude={"roles"})


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
