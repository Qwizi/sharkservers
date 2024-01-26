"""
Module contains the models for users, user sessions, and bans in the SharkServers API.

The User model represents a user in the system and includes fields such as username, email, password, and various statistics like threads_count, posts_count, and likes_count. It also has relationships with roles, player, and sessions.

The UserSession model represents a session of a user and includes fields for user IP and user agent.

The Ban model represents a ban on a user and includes fields for the banned user, reason, ban time, and the user who issued the ban.

The module also includes a pre_update hook for the User model that updates the "updated_at" field whenever a user is updated.
"""
from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

import ormar

from sharkservers.auth.utils import now_datetime
from sharkservers.db import BaseMeta, DateFieldsMixins
from sharkservers.players.models import Player
from sharkservers.roles.models import Role

if TYPE_CHECKING:
    import datetime

    from pydantic import EmailStr


class UserSession(ormar.Model, DateFieldsMixins):
    """
    Represent a user session.

    Attributes
    ----------
        id (str): The unique identifier for the user session.
        user_ip (str): The IP address of the user.
        user_agent (str): The user agent string of the client.
    """

    class Meta(BaseMeta):
        """Meta class for defining metadata options for the UserSessions model."""

        tablename = "user_sessions"

    id: str = ormar.UUID(primary_key=True, default=uuid.uuid4)
    user_ip: str = ormar.String(max_length=255)
    user_agent: str = ormar.String(max_length=255)


class User(ormar.Model, DateFieldsMixins):
    """
    Represents a user in the system.

    Attributes
    ----------
        id (int): The unique identifier of the user.
        username (str, optional): The username of the user. Max length is 64 characters.
        email (str, optional): The email address of the user. Max length is 255 characters.
        password (str, optional): The password of the user. Max length is 255 characters.
        is_activated (bool, optional): Indicates if the user is activated.
        is_superuser (bool, optional): Indicates if the user is a superuser.
        avatar (str, optional): The path to the user's avatar image.
        roles (List[Role], optional): The roles assigned to the user.
        display_role (Role, optional): The role to be displayed for the user.
        last_login (datetime.datetime, optional): The timestamp of the user's last login.
        last_online (datetime.datetime, optional): The timestamp of the user's last online activity.
        secret_salt (str, optional): The secret salt used for password hashing. Max length is 255 characters.
        threads_count (int): The number of threads created by the user.
        posts_count (int): The number of posts created by the user.
        likes_count (int): The number of likes received by the user.
        player (Player, optional): The associated player for the user.
        sessions (List[UserSession], optional): The sessions associated with the user.
    """

    class Meta(BaseMeta):
        """Meta class for defining metadata options for the User model."""

        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    username: str | None = ormar.String(max_length=64, unique=True)
    email: EmailStr | None = ormar.String(max_length=255, unique=True)
    password: str | None = ormar.String(max_length=255)
    is_activated: bool | None = ormar.Boolean(default=False)
    is_superuser: bool | None = ormar.Boolean(default=False)
    avatar: str | None = ormar.String(
        max_length=255,
        default="/static/avatars/avatars/default_avatar.png",
    )
    roles: list[Role] | None = ormar.ManyToMany(Role, related_name="user_roles")
    display_role: Role | None = ormar.ForeignKey(
        Role,
        related_name="user_display_role",
    )
    last_login: datetime.datetime | None = ormar.DateTime(nullable=True)
    last_online: datetime.datetime | None = ormar.DateTime(nullable=True)
    secret_salt: str | None = ormar.String(max_length=255, unique=True)
    threads_count: int = ormar.Integer(default=0)
    posts_count: int = ormar.Integer(default=0)
    likes_count: int = ormar.Integer(default=0)
    player: Player | None = ormar.ForeignKey(Player, related_name="player")
    sessions: UserSession | None = ormar.ManyToMany(
        UserSession,
        related_name="users_sessions",
    )


class Ban(ormar.Model, DateFieldsMixins):
    """
    Represent a ban in the system.

    Attributes
    ----------
        id (int): The unique identifier for the ban.
        user (Optional[User]): The user who is banned.
        reason (Optional[str]): The reason for the ban.
        ban_time (Optional[datetime.datetime]): The time when the ban was imposed.
        banned_by (Optional[User]): The user who imposed the ban.
    """

    class Meta(BaseMeta):
        """Meta class for defining metadata options for the Ban model."""

        tablename = "banned"

    id: int = ormar.Integer(primary_key=True)
    user: User | None = ormar.ForeignKey(User, related_name="banned_user")
    reason: str | None = ormar.String(max_length=255)
    ban_time: datetime.datetime | None = ormar.DateTime(nullable=True, timezone=True)
    banned_by: User | None = ormar.ForeignKey(User, related_name="banned_by")


@ormar.pre_update(User)
async def update_user_updated_at(
    sender, instance: User, **kwargs
) -> None:  # noqa: ARG001, ANN001, ANN003
    """
    Update the 'updated_at' field of a User instance with the current datetime.

    Args:
    ----
        sender: The sender of the signal.
        instance: The User instance being updated.
        kwargs: Additional keyword arguments.
    """
    instance.updated_at = now_datetime()
