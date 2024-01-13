"""Enums for forum app."""  # noqa: EXE002
from enum import Enum


class CategoryExceptionEnum(str, Enum):
    """Enum for categories exceptions."""

    NOT_FOUND = "Category not found"
    ALREADY_EXISTS = "Category already exists"
    NOT_ALLOWED = "You are not allowed to create a category"


class TagExceptionEnum(str, Enum):
    """Enum for tags exceptions."""

    NOT_FOUND = "Tag not found"


class ThreadExceptionEnum(str, Enum):
    """Enum for thread exceptions."""

    NOT_FOUND = "Thread not found"
    ALREADY_EXISTS = "Thread with this title on this category exists"
    IS_CLOSED = "Thread is closed"
    NOT_VALID_THREAD_AUTHOR = "You are not allowed to update this thread"


class PostExceptionsEnum(str, Enum):
    """Enum for post exceptions."""

    NOT_FOUND = "Post not found"
    ALREADY_EXISTS = "Post already exists"
    NOT_VALID_AUTHOR = "You are not allowed to update this post"


class LikeExceptionsEnum(str, Enum):
    """Enum for like exceptions."""

    NOT_FOUND = "Like not found"
    ALREADY_EXISTS = "U already liked this post"


class CategoryEventEnum(str, Enum):
    """Enum for categories events."""

    GET_ALL_PRE = "CATEGORIES_GET_ALL_PRE"
    GET_ALL_POST = "CATEGORIES_GET_ALL_POST"
    GET_ONE_PRE = "CATEGORIES_GET_ONE_PRE"
    GET_ONE_POST = "CATEGORIES_GET_ONE_POST"


class CategoryAdminEventEnum(str, Enum):
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


class TagEventsEnum(str, Enum):
    """Enum for tags events."""

    GET_ALL_PRE = "TAGS_GET_ALL_PRE"
    GET_ALL_POST = "TAGS_GET_ALL_POST"
    GET_ONE_PRE = "TAGS_GET_ONE_PRE"
    GET_ONE_POST = "TAGS_GET_ONE_POST"


class TagAdminEventsEnum(str, Enum):
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


class ThreadEventEnum(str, Enum):
    """Enum for threads events."""

    GET_ALL_PRE = "THREADS_GET_ALL_PRE"
    GET_ALL_POST = "THREADS_GET_ALL_POST"
    GET_ONE_PRE = "THREADS_GET_ONE_PRE"
    GET_ONE_POST = "THREADS_GET_ONE_POST"
    CREATE_PRE = "THREADS_CREATE_PRE"
    CREATE_POST = "THREADS_CREATE_POST"
    UPDATE_PRE = "THREADS_UPDATE_PRE"
    UPDATE_POST = "THREADS_UPDATE_POST"
    DELETE_PRE = "THREADS_DELETE_PRE"
    DELETE_POST = "THREADS_DELETE_POST"
    CLOSE_PRE = "THREADS_CLOSE_PRE"
    CLOSE_POST = "THREADS_CLOSE_POST"
    OPEN_PRE = "THREADS_OPEN_PRE"
    OPEN_POST = "THREADS_OPEN_POST"


class ThreadAdminEventEnum(str, Enum):
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


class PostEventEnum(str, Enum):
    """Enum for posts events."""

    GET_ALL_PRE = "POSTS_GET_ALL_PRE"
    GET_ALL_POST = "POSTS_GET_ALL_POST"
    GET_ONE_PRE = "POSTS_GET_ONE_PRE"
    GET_ONE_POST = "POSTS_GET_ONE_POST"
    CREATE_PRE = "POSTS_CREATE_PRE"
    CREATE_POST = "POSTS_CREATE_POST"
    UPDATE_PRE = "POSTS_UPDATE_PRE"
    UPDATE_POST = "POSTS_UPDATE_POST"
    DELETE_PRE = "POSTS_DELETE_PRE"
    DELETE_POST = "POSTS_DELETE_POST"


# create PostAdminEventEnum
class PostAdminEventEnum(str, Enum):
    """Enum for posts admin events."""

    GET_ALL_PRE = "POSTS_ADMIN_GET_ALL_PRE"
    GET_ALL_POST = "POSTS_ADMIN_GET_ALL_POST"
    GET_ONE_PRE = "POSTS_ADMIN_GET_ONE_PRE"
    GET_ONE_POST = "POSTS_ADMIN_GET_ONE_POST"
    CREATE_PRE = "POSTS_ADMIN_CREATE_PRE"
    CREATE_POST = "POSTS_ADMIN_CREATE_POST"
    UPDATE_PRE = "POSTS_ADMIN_UPDATE_PRE"
    UPDATE_POST = "POSTS_ADMIN_UPDATE_POST"
    DELETE_PRE = "POSTS_ADMIN_DELETE_PRE"
    DELETE_POST = "POSTS_ADMIN_DELETE_POST"


class CategoryTypeEnum(str, Enum):
    """Enum for category types."""

    PUBLIC = "public"
    PRIVATE = "private"
    APPLICATION = "application"
    APPEAL = "appeal"


class ThreadTypeEnum(str, Enum):
    """Enum for thread types."""

    APPLICATION = "application"
    APPEAL = "appeal"


class ThreadStatusEnum(str, Enum):
    """Enum for thread statuses."""

    APPROVED = "approved"
    PENDING = "pending"
    REJECTED = "rejected"


class ThreadOrderEnum(str, Enum):
    """Enum for thread order."""

    ID_DESC = "-id"
    ID_ASC = "id"


class ThreadActionEnum(str, Enum):
    """Enum for thread actions."""

    CLOSE = "close"
    OPEN = "open"
    APPROVE = "approve"
    REJECT = "reject"
    MOVE = "move"
    PIN = "pin"
    UNPIN = "unpin"
