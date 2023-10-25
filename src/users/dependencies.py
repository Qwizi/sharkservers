from uuid import UUID
from fastapi import Depends
from ormar import NoMatch, Model

from src.users.exceptions import user_not_found_exception
from src.users.services import UserService, UserSessionService


async def get_users_service() -> UserService:
    """
    Get users service
    :return users_service:
    """
    return UserService()


async def get_valid_user(
    user_id: int, users_service: UserService = Depends(get_users_service)
) -> Model:
    """
    Validate user id
    :param users_service:
    :param user_id:
    :return User:
    """
    try:
        return await users_service.get_one(
            id=user_id,
            related=["roles", "display_role", "player", "player__steamrep_profile"],
        )
    except NoMatch:
        raise user_not_found_exception


async def get_users_sessions_service() -> UserSessionService:
    return UserSessionService()


async def get_valid_user_session(
    session_id: UUID,
    users_sessions_service: UserSessionService = Depends(get_users_sessions_service)
):
    try:
        return await users_sessions_service.get_one(
            id=session_id,
        )
    except NoMatch:
        raise user_not_found_exception
