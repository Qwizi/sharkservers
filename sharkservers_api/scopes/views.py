from fastapi import APIRouter, Depends
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Page, Params
from fastapi_pagination.bases import AbstractPage

from src.scopes.dependencies import get_scopes_service
from src.scopes.enums import ScopesEventsEnum
from src.scopes.schemas import ScopeOut
from src.scopes.services import ScopeService

router = APIRouter()


@router.get("", response_model=Page[ScopeOut], response_model_exclude_none=True)
async def get_all_scopes(
    params: Params = Depends(),
    scopes_service: ScopeService = Depends(get_scopes_service),
    role_id: int = None,
) -> AbstractPage[ScopeOut]:
    """
    Get all scopes

    :param scopes_service:
    :param params:
    :param role_id:
    :return:
    """
    dispatch(
        ScopesEventsEnum.GET_ALL_PRE,
        payload={"data": {"params": params, "role_id": role_id}},
    )
    scopes = []
    if role_id:
        scopes = await scopes_service.get_all(
            params=params, related=["roles"], roles__id=role_id
        )
    else:
        scopes = await scopes_service.get_all(params=params)
    dispatch(ScopesEventsEnum.GET_ALL_POST, payload={"data": scopes})
    return scopes
