"""Scopes admin views."""
from fastapi import APIRouter, Depends, Security
from fastapi_pagination import Page, Params

from sharkservers.auth.dependencies import get_admin_user
from sharkservers.scopes.dependencies import get_scopes_service, get_valid_scope
from sharkservers.scopes.models import Scope
from sharkservers.scopes.schemas import CreateScopeSchema, ScopeOut, UpdateScopeSchema
from sharkservers.scopes.services import ScopeService

router = APIRouter()


@router.get("", dependencies=[Security(get_admin_user, scopes="scopes:all")])
async def admin_get_scopes(
    params: Params = Depends(),
    scopes_service: ScopeService = Depends(get_scopes_service),
) -> Page[ScopeOut]:
    """
    Retrieve all scopes for admin users.

    Args:
    ----
        params (Params): The parameters for filtering and pagination.
        scopes_service (ScopeService): The service for retrieving scopes.

    Returns:
    -------
        Page[ScopeOut]: A paginated list of ScopeOut objects.
    """
    return await scopes_service.get_all(params=params)


@router.get(
    "/{scope_id}",
    dependencies=[Security(get_admin_user, scopes="scopes:retrieve")],
)
async def admin_get_scope(
    scope: Scope = Depends(get_valid_scope),
) -> ScopeOut:
    """
    Retrieve a scope for admin users.

    Args:
    ----
        scope (Scope): The scope to retrieve.

    Returns:
    -------
        ScopeOut: The retrieved scope.
    """
    return scope


@router.post("", dependencies=[Security(get_admin_user, scopes="scopes:create")])
async def admin_create_scope(
    scope_data: CreateScopeSchema,
    scopes_service: ScopeService = Depends(get_scopes_service),
) -> ScopeOut:
    """
    Create a new scope.

    Args:
    ----
        scope_data (CreateScopeSchema): The data for creating the scope.
        scopes_service (ScopeService, optional): The service for managing scopes. Defaults to Depends(get_scopes_service).

    Returns:
    -------
        ScopeOut: The created scope.
    """
    return await scopes_service.create(**scope_data.dict())


@router.delete(
    "/{scope_id}",
    dependencies=[Security(get_admin_user, scopes="scopes:delete")],
)
async def admin_delete_scope(
    scope: Scope = Depends(get_valid_scope),
    scopes_service: ScopeService = Depends(get_scopes_service),
) -> ScopeOut:
    """
    Deletes a scope from the system.

    Args:
    ----
        scope (Scope): The scope to be deleted.
        scopes_service (ScopeService): The service responsible for managing scopes.

    Returns:
    -------
        ScopeOut: The deleted scope.
    """  # noqa: D401
    return await scopes_service.delete(_id=scope.id)


@router.put(
    "/{scope_id}",
    dependencies=[Security(get_admin_user, scopes="scopes:update")],
)
async def admin_update_scope(
    update_scope_data: UpdateScopeSchema,
    scope: Scope = Depends(get_valid_scope),
) -> ScopeOut:
    """
    Update the given scope with the provided data.

    Args:
    ----
        update_scope_data (UpdateScopeSchema): The data to update the scope with.
        scope (Scope): The scope to be updated.

    Returns:
    -------
        ScopeOut: The updated scope.
    """
    await scope.update(**update_scope_data.dict(exclude_unset=True, exclude_none=True))
    return scope
