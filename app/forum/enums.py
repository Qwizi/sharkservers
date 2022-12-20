from enum import Enum


class CategoriesExceptionsEnum(str, Enum):
    """Enum for categories exceptions."""
    NOT_FOUND = "Category not found"
    ALREADY_EXISTS = "Category already exists"
    NOT_ALLOWED = "You are not allowed to create a category"


class TagsExceptionsEnum(str, Enum):
    """Enum for tags exceptions."""
    NOT_FOUND = "Tag not found"


class ThreadsExceptionsEnum(str, Enum):
    """Enum for thread exceptions."""
    NOT_FOUND = "Thread not found"
    ALREADY_EXISTS = "Thread with this title on this category exists"


class CategoriesEventsEnum(str, Enum):
    """Enum for categories events."""
    GET_ALL_PRE = "CATEGORIES_GET_ALL_PRE"
    GET_ALL_POST = "CATEGORIES_GET_ALL_POST"
    GET_ONE_PRE = "CATEGORIES_GET_ONE_PRE"
    GET_ONE_POST = "CATEGORIES_GET_ONE_POST"


class CategoriesAdminEventsEnum(str, Enum):
    """Enum for categories admin events."""
    GET_ALL_PRE = "CATEGORIES_ADMIN_GET_ALL_PRE"
    GET_ALL_POST = "CATEGORIES_ADMIN_GET_ALL_POST"
    GET_ONE_PRE = "CATEGORIES_ADMIN_GET_ONE_PRE"
    GET_ONE_POST = "CATEGORIES_ADMIN_GET_ONE_POST"
    CREATE_PRE = "CATEGORIES_ADMIN_CREATE_PRE"
    CREATE_POST = "CATEGORIES_ADMIN_CREATE_POST"
    UPDATE_PRE = "CATEGORIES_ADMIN_UPDATE_PRE"
    UPDATE_POST = "CATEGORIES_ADMIN_UPDATE_POST"
    DELETE_PRE = "CATEGORIES_ADMIN_DELETE_PRE"
    DELETE_POST = "CATEGORIES_ADMIN_DELETE_POST"


class TagsEventsEnum(str, Enum):
    """Enum for tags events."""
    GET_ALL_PRE = "TAGS_GET_ALL_PRE"
    GET_ALL_POST = "TAGS_GET_ALL_POST"
    GET_ONE_PRE = "TAGS_GET_ONE_PRE"
    GET_ONE_POST = "TAGS_GET_ONE_POST"


class TagsAdminEventsEnum(str, Enum):
    """Enum for tags admin events."""
    GET_ALL_PRE = "TAGS_ADMIN_GET_ALL_PRE"
    GET_ALL_POST = "TAGS_ADMIN_GET_ALL_POST"
    GET_ONE_PRE = "TAGS_ADMIN_GET_ONE_PRE"
    GET_ONE_POST = "TAGS_ADMIN_GET_ONE_POST"
    CREATE_PRE = "TAGS_ADMIN_CREATE_PRE"
    CREATE_POST = "TAGS_ADMIN_CREATE_POST"
    UPDATE_PRE = "TAGS_ADMIN_UPDATE_PRE"
    UPDATE_POST = "TAGS_ADMIN_UPDATE_POST"
    DELETE_PRE = "TAGS_ADMIN_DELETE_PRE"
    DELETE_POST = "TAGS_ADMIN_DELETE_POST"


class ThreadsEventsEnum(str, Enum):
    """Enum for threads events."""
    GET_ALL_PRE = "THREADS_GET_ALL_PRE"
    GET_ALL_POST = "THREADS_GET_ALL_POST"
    GET_ONE_PRE = "THREADS_GET_ONE_PRE"
    GET_ONE_POST = "THREADS_GET_ONE_POST"


class ThreadsAdminEventsEnum(str, Enum):
    """Enum for threads admin events."""
    GET_ALL_PRE = "THREADS_ADMIN_GET_ALL_PRE"
    GET_ALL_POST = "THREADS_ADMIN_GET_ALL_POST"
    GET_ONE_PRE = "THREADS_ADMIN_GET_ONE_PRE"
    GET_ONE_POST = "THREADS_ADMIN_GET_ONE_POST"
    CREATE_PRE = "THREADS_ADMIN_CREATE_PRE"
    CREATE_POST = "THREADS_ADMIN_CREATE_POST"
    UPDATE_PRE = "THREADS_ADMIN_UPDATE_PRE"
    UPDATE_POST = "THREADS_ADMIN_UPDATE_POST"
    DELETE_PRE = "THREADS_ADMIN_DELETE_PRE"
    DELETE_POST = "THREADS_ADMIN_DELETE_POST"
