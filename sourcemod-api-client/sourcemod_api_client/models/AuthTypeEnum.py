from enum import Enum


class AuthTypeEnum(str, Enum):
    steam = "steam"
    name = "name"
    ip = "ip"
