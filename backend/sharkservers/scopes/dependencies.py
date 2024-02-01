"""Dependencies for scopes endpoints."""

from fastapi import Depends

from sharkservers.scopes.models import Scope
from sharkservers.scopes.services import ScopeService


async def get_scopes_service() -> ScopeService:
    """Get the ScopeService instance."""
    return ScopeService()


async def get_valid_scope(
    scope_id: int,
    scopes_service: ScopeService = Depends(get_scopes_service),
) -> Scope:
    """Get a valid scope by ID."""
    return await scopes_service.get_one(id=scope_id)
