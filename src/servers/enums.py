from enum import Enum


class ServerExceptionEnum(str, Enum):
    NOT_FOUND = "Server not found"


class ChatColorModuleExceptionEnum(str, Enum):
    NOT_FOUND = "Chat color not found"
