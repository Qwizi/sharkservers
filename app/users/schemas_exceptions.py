from app.schemas import HTTPError404Schema
from app.users.exceptions import UserNotFound


class UserNotFoundSchema(HTTPError404Schema):
    detail = UserNotFound().detail
