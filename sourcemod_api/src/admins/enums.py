
from enum import Enum


class AuthTypeEnum(str, Enum):
    STEAM = "steam"
    NAME = "name"
    IP = "ip"

class GroupOverrideTypeEnum(str, Enum):
    COMMAND = "command"
    GROUP = "group"


class GroupOverrideAccessEnum(str, Enum):
    ALLOW = "allow"
    DENY = "deny"