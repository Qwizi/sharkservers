from enum import Enum


class ScopeEnum(Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    RETRIEVE = "retrieve"
    ALL = "all"
    ADMIN_CREATE = "a:create"
    ADMIN_UPDATE = "a:update"
    ADMIN_DELETE = "a:delete"
    ADMIN_RETRIEVE = "a:retrieve"
    ADMIN_ALL = "a:all"


class ScopesExceptionsDetailEnum(str, Enum):
    """Scopes exceptions detail enum."""

    NOT_FOUND = "Scope not found"


class ScopesEventsEnum(str, Enum):
    """Scopes events enum."""

    GET_ALL_PRE = "SCOPES_GET_ALL_PRE"
    GET_ALL_POST = "SCOPES_GET_ALL_POST"
    GET_ONE_PRE = "SCOPES_GET_ONE_PRE"
    GET_ONE_POST = "SCOPES_GET_ONE_POST"


class ScopesAdminEventsEnum(str, Enum):
    """Scopes events enum."""

    GET_ALL_PRE = "SCOPES_ADMIN_GET_ALL_PRE"
    GET_ALL_POST = "SCOPES_ADMIN_GET_ALL_POST"
    GET_ONE_PRE = "SCOPES_ADMIN_GET_ONE_PRE"
    GET_ONE_POST = "SCOPES_ADMIN_GET_ONE_POST"
    CREATE_PRE = "SCOPES_ADMIN_CREATE_PRE"
    CREATE_POST = "SCOPES_ADMIN_CREATE_POST"
    DELETE_PRE = "SCOPES_ADMIN_DELETE_PRE"
    DELETE_POST = "SCOPES_ADMIN_DELETE_POST"
