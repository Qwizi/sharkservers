"""Scopes views."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params

from sharkservers.scopes.dependencies import get_scopes_service
from sharkservers.scopes.schemas import ScopeOut
from sharkservers.scopes.services import ScopeService

router = APIRouter()


@router.get("", response_model_exclude_none=True)
async def get_all_scopes(
    params: Params = Depends(),
    scopes_service: ScopeService = Depends(get_scopes_service),
    role_id: int | None = None,
) -> Page[ScopeOut]:
    """
    Retrieve all scopes.

    Args:
    ----
        params (Params, optional): The request parameters. Defaults to Depends().
        scopes_service (ScopeService, optional): The scope service. Defaults to Depends(get_scopes_service).
        role_id (int | None, optional): The role ID. Defaults to None.

    Returns:
    -------
        Page[ScopeOut]: The list of scopes.
    """
    scopes = []
    if role_id:
        scopes = await scopes_service.get_all(
            params=params,
            related=["roles"],
            roles__id=role_id,
        )
    else:
        scopes = await scopes_service.get_all(params=params)
    return scopes
