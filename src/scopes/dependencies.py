from src.scopes.services import ScopeService


async def get_scopes_service() -> ScopeService:
    return ScopeService()
