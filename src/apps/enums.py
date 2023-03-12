# apps enums
from enum import Enum


class AppsExceptionEnum(str, Enum):
    NOT_FOUND = "Apps not found"


class AppsEventsEnum(str, Enum):
    """RApps events enum."""

    GET_ALL = "APPS_GET_ALL"
    GET_ONE = "APPS_GET_ONE"
    CREATE = "APPS_CREATE"
    UPDATE = "APPS_UPDATE"
    DELETE = "APPS_DELETE"
    ADMIN_GET_ALL = "APPS_ADMIN_GET_ALL"
    ADMIN_GET_ONE = "APPS_ADMIN_GET_ONE"
    ADMIN_CREATE = "APPS_ADMIN_CREATE"
    ADMIN_UPDATE = "APPS_ADMIN_UPDATE"
    ADMIN_DELETE = "APPS_ADMIN_DELETE"



