"""
Module contains dependency functions for user-related operations.

Dependencies are functions that are used to inject objects or services into other functions or endpoints.
These functions are used as parameters in FastAPI's `Depends` decorator.

Functions:
- get_users_service: Returns an instance of the UserService class.
- get_valid_user: Validates a user ID and returns the corresponding user model.
- get_users_sessions_service: Returns an instance of the UserSessionService class.
- get_valid_user_session: Validates a user session ID and returns the corresponding user session model.
"""  # noqa: EXE002, E501
from uuid import UUID

from fastapi import Depends
from ormar import Model, NoMatch

from sharkservers.users.exceptions import user_not_found_exception
from sharkservers.users.models import UserSession
from sharkservers.users.services import UserService, UserSessionService


async def get_users_service() -> UserService:
    """
    Return an instance of the UserService class.

    Returns
    -------
        UserService: An instance of the UserService class.
    """
    return UserService()


async def get_valid_user(
    user_id: int,
    users_service: UserService = Depends(get_users_service),  # noqa: B008
) -> Model:
    """
    Retrieves a valid user by their ID.

    Args:
    ----
        user_id (int): The ID of the user.
        users_service (UserService, optional): The user service dependency. Defaults to Depends(get_users_service).

    Returns:
    -------
        Model: The user model.

    Raises:
    ------
        user_not_found_exception: If the user is not found.
    """  # noqa: D401, E501
    try:
        return await users_service.get_one(
            id=user_id,
            related=["roles", "display_role", "player", "player__steamrep_profile"],
        )
    except NoMatch as err:
        raise user_not_found_exception from err


async def get_users_sessions_service() -> UserSessionService:
    """
    Get the UserSessionService instance.

    Returns
    -------
        UserSessionService: The UserSessionService instance.
    """
    return UserSessionService()


async def get_valid_user_session(
    session_id: UUID,
    users_sessions_service: UserSessionService = Depends(get_users_sessions_service),  # noqa: B008
) -> UserSession:
    """
    Retrieve a valid user session by session ID.

    Args:
    ----
        session_id (UUID): The ID of the session to retrieve.
        users_sessions_service (UserSessionService, optional): The user sessions service. Defaults to the result of `get_users_sessions_service`.

    Returns:
    -------
        UserSession: The retrieved user session.

    Raises:
    ------
        user_not_found_exception: If the user session is not found.
    """  # noqa: E501
    try:
        return await users_sessions_service.get_one(
            id=session_id,
        )
    except NoMatch:
        raise user_not_found_exception from None
