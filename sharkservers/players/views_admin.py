"""Admin views for players."""  # noqa: EXE002

from fastapi import APIRouter, BackgroundTasks, Depends, Security
from fastapi_pagination import Page, Params
from ormar import NoMatch

from sharkservers.auth.dependencies import get_admin_user
from sharkservers.players.dependencies import get_players_service
from sharkservers.players.exceptions import player_not_found_exception
from sharkservers.players.models import Player
from sharkservers.players.schemas import CreatePlayerSchema, PlayerOut
from sharkservers.players.services import PlayerService

router = APIRouter()


@router.get("", dependencies=[Security(get_admin_user, scopes=["players:all"])])
async def admin_get_steam_profiles(
    params: Params = Depends(),  # noqa: B008
    players_service: PlayerService = Depends(get_players_service),  # noqa: B008
) -> Page[PlayerOut]:
    """
    Retrieve all player profiles with their associated SteamRep profiles.

    Args:
    ----
        params (Params): The parameters for filtering and pagination.
        players_service (PlayerService): The service for retrieving player profiles.

    Returns:
    -------
        Page[PlayerOut]: A paginated list of player profiles with their associated SteamRep profiles.
    """  # noqa: E501
    return await players_service.get_all(params, related=["steamrep_profile"])


@router.get(
    "/{profile_id}",
    dependencies=[Security(get_admin_user, scopes=["players:all"])],
)
async def admin_get_steam_profile(
    profile_id: int,
) -> PlayerOut:
    """
    Retrieve the Steam profile of a player with the given profile ID.

    Args:
    ----
        profile_id (int): The ID of the player's Steam profile.

    Returns:
    -------
        PlayerOut: The player's Steam profile.

    Raises:
    ------
        player_not_found_exception: If the player's profile is not found.
    """
    try:
        return await Player.objects.get(id=profile_id)
    except NoMatch:
        raise player_not_found_exception  # noqa: B904


@router.post("", dependencies=[Security(get_admin_user, scopes=["players:all"])])
async def admin_create_player(
    profile_data: CreatePlayerSchema,
    background_tasks: BackgroundTasks,
    players_service: PlayerService = Depends(get_players_service),  # noqa: B008
) -> dict:
    """
    Admin endpoint to create a player.

    Args:
    ----
        profile_data (CreatePlayerSchema): The data for creating a player.
        background_tasks (BackgroundTasks): The background tasks object.
        players_service (PlayerService, optional): The player service dependency. Defaults to Depends(get_players_service).

    Returns:
    -------
        dict: A dictionary with a message indicating that the player was created.
    """  # noqa: E501
    background_tasks.add_task(
        players_service.create_player,
        profile_data.dict()["steamid64"],
    )
    return {"msg": "Player created"}


@router.delete(
    "/{profile_id}", dependencies=[Security(get_admin_user, scopes=["players:all"])]
)  # noqa: E501
async def admin_delete_steam_profile(
    profile_id: int,
) -> PlayerOut:
    """
    Delete a Steam profile with the given profile ID.

    Args:
    ----
        profile_id (int): The ID of the profile to delete.

    Returns:
    -------
        PlayerOut: The deleted player profile.

    Raises:
    ------
        player_not_found_exception: If the player profile with the given ID is not found.
    """  # noqa: E501
    try:
        profile = await Player.objects.get(id=profile_id)
        await profile.delete()
        return profile  # noqa: TRY300
    except NoMatch as err:
        raise player_not_found_exception from err
