from ormar import NoMatch

from src.users.exceptions import user_not_found_exception
from src.users.models import User
from src.users.services import users_service


async def get_valid_user(user_id: int) -> User:
    """
    Validate user id
    :param user_id:
    :return User:
    """
    try:
        return await users_service.get_one(
            id=user_id, related=["roles", "display_role"]
        )
    except NoMatch:
        raise user_not_found_exception
