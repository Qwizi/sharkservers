"""Dependencies for scopes endpoints."""

from fastapi import Depends
from uuidbase62 import UUIDBase62, get_validated_uuidbase62_by_model

from sharkservers.scopes.models import Scope
from sharkservers.scopes.schemas import ScopeOut
from sharkservers.scopes.services import ScopeService


async def get_scopes_service() -> ScopeService:
    """Get the ScopeService instance."""
    return ScopeService()


async def get_valid_scope(
    scope_id: UUIDBase62 = Depends(
        get_validated_uuidbase62_by_model(ScopeOut, "id", "scope_id"),
    ),
    scopes_service: ScopeService = Depends(get_scopes_service),
) -> Scope:
    """Get a valid scope by ID."""
    return await scopes_service.get_one(id=scope_id.uuid)
