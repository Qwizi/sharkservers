from fastapi import Depends
from src.scopes.services import ScopeService


async def get_scopes_service() -> ScopeService:
    return ScopeService()


async def get_valid_scope(
    scope_id: int, scopes_service: ScopeService = Depends(get_scopes_service)
):
    return await scopes_service.get_one(id=scope_id)
