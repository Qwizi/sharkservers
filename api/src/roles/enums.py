from enum import Enum


class ProtectedDefaultRolesEnum(int, Enum):
    ADMIN = 1
    USER = 2
    BANNED = 3
    VIP = 4

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
    

class ProtectedDefaultRolesTagEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"
    BANNED = "banned"
    VIP = "vip"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class RolesExceptionsDetailEnum(str, Enum):
    """Roles exceptions detail enum."""

    NOT_FOUND = "Role not found"
    ALREADY_EXISTS = "Role already exists"
    PROTECTED = "U cannot delete protected role"


class RolesEventsEnum(str, Enum):
    """Roles events enum."""

    GET_ALL_PRE = "ROLES_GET_ALL_PRE"
    GET_ALL_POST = "ROLES_GET_ALL_POST"
    GET_ONE_PRE = "ROLES_GET_ONE_PRE"
    GET_ONE_POST = "ROLES_GET_ONE_POST"
    STAFF_GET_ALL_PRE = "ROLES_STAFF_GET_ALL_PRE"
    STAFF_GET_ALL_POST = "ROLES_STAFF_GET_ALL_POST"


class RolesAdminEventsEnum(str, Enum):
    """Roles admin events enum."""

    GET_ALL_PRE = "ROLES_ADMIN_GET_ALL_PRE"
    GET_ALL_POST = "ROLES_ADMIN_GET_ALL_POST"
    GET_ONE_PRE = "ROLES_ADMIN_GET_ONE_PRE"
    GET_ONE_POST = "ROLES_ADMIN_GET_ONE_POST"
    CREATE_PRE = "ROLES_ADMIN_CREATE_PRE"
    CREATE_POST = "ROLES_ADMIN_CREATE_POST"
    UPDATE_PRE = "ROLES_ADMIN_UPDATE_PRE"
    UPDATE_POST = "ROLES_ADMIN_UPDATE_POST"
    DELETE_PRE = "ROLES_ADMIN_DELETE_PRE"
    DELETE_POST = "ROLES_ADMIN_DELETE_POST"
