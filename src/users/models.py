import datetime
from typing import Optional, List

import ormar
from pydantic import EmailStr
from src.players.models import Player
from src.auth.utils import now_datetime

from src.db import BaseMeta, DateFieldsMixins
from src.roles.models import Role


class User(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    username: Optional[str] = ormar.String(max_length=64, unique=True)
    email: Optional[EmailStr] | None = ormar.String(max_length=255, unique=True)
    password: Optional[str] = ormar.String(max_length=255)
    is_activated: Optional[bool] = ormar.Boolean(default=False)
    is_superuser: Optional[bool] = ormar.Boolean(default=False)
    avatar: Optional[str] = ormar.String(
        max_length=255, default="/static/avatars/avatars/default_avatar.png"
    )
    roles: Optional[List[Role]] = ormar.ManyToMany(Role, related_name="user_roles")
    display_role: Optional[Role] = ormar.ForeignKey(
        Role, related_name="user_display_role"
    )
    last_login: Optional[datetime.datetime] = ormar.DateTime(nullable=True)
    last_online: Optional[datetime.datetime] = ormar.DateTime(nullable=True)
    secret_salt: Optional[str] = ormar.String(max_length=255, unique=True)
    threads_count: int = ormar.Integer(default=0)
    posts_count: int = ormar.Integer(default=0)
    likes_count: int = ormar.Integer(default=0)
    player: Optional[Player] = ormar.ForeignKey(Player, related_name="player")


class Ban(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "banned"

    id: int = ormar.Integer(primary_key=True)
    user: Optional[User] = ormar.ForeignKey(User, related_name="banned_user")
    reason: Optional[str] = ormar.String(max_length=255)
    ban_time: Optional[datetime.datetime] = ormar.DateTime(nullable=True, timezone=True)
    banned_by: Optional[User] = ormar.ForeignKey(User, related_name="banned_by")



@ormar.pre_update(User)
async def update_user_updated_at(sender, instance: User, **kwargs):
    instance.updated_at = now_datetime()
