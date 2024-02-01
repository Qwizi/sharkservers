"""Server enums."""
from enum import Enum


class ServerExceptionEnum(str, Enum):
    """Enum class for server exceptions."""

    NOT_FOUND = "Server not found"


class ChatColorModuleExceptionEnum(str, Enum):
    """Enum class for chat color module exceptions."""

    NOT_FOUND = "Chat color not found"
