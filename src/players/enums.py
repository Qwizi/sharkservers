from enum import Enum


class PlayerEventEnum(str, Enum):
    """Player event enum"""
    CREATE = 'player_create'
    CREATED = "player_created"
    UPDATED = "player_updated"
    DELETED = "player_deleted"
