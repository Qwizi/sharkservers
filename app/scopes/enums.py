from enum import Enum


class ScopeEnum(Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    RETRIEVE = "retrieve"
    GET = "get"
    GET_ALL = "get_all"
