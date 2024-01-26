"""Forum schemas."""
from __future__ import annotations

from fastapi import Query
from pydantic import BaseModel, Field

from sharkservers.forum.enums import (
    CategoryTypeEnum,
    ThreadActionEnum,
    ThreadStatusEnum,
)
from sharkservers.forum.models import Category, Like, Post, Thread, ThreadMeta
from sharkservers.roles.models import Role
from sharkservers.schemas import OrderQuery

author_exclude = {
    "author__password",
    "author__email",
    "author__display_role__scopes",
    "author__secret_salt",
    "author__roles",
    "author__apps",
    "author__banned_by",
    "author__banned_user",
    "author__players",
    "author__chats",
    "author__sessions",
    "author__user_posts",
}

category_out = Category.get_pydantic(exclude={"threads"})
thread_out = Thread.get_pydantic(
    exclude=author_exclude
    | {"posts", "server__server_chat_color_module", "server__admin_role__scopes"},
)
post_out = Post.get_pydantic(exclude=author_exclude | {"likes", "thread_post"})
like_out = Like.get_pydantic(exclude=author_exclude | {"post_likes"})
thread_meta_out = ThreadMeta.get_pydantic()


class CategoryOut(category_out):
    """Category output schema."""

    class Config:
        """Category output schema config."""

        orm_mode = True


class ThreadMetaOut(BaseModel):
    """Thread meta output schema."""

    class Config:
        """Thread meta output schema config."""

        orm_mode = True


class ThreadOut(thread_out):
    """Thread output schema."""

    class Config:
        """Thread output schema config."""

        orm_mode = True


class PostOut(post_out):
    """Post output schema."""

    class Config:
        """Post output schema config."""

        orm_mode = True


class LikeOut(like_out):
    """Like output schema."""

    class Config:
        """Like output schema config."""

        orm_mode = True


class ThreadTag(BaseModel):
    """Thread tag schema."""

    id: int
    name: str


class ThreadCategory(BaseModel):
    """Thread category schema."""

    id: int
    name: str


class ThreadAuthor(BaseModel):
    """Thread author schema."""

    id: int
    username: str
    avatar: str
    display_role: Role


class ThreadPostSchema(BaseModel):
    """Thread post schema."""

    id: int
    content: str
    author: ThreadAuthor


class AdminCreateCategorySchema(BaseModel):
    """Admin create category schema."""

    title: str = Field(max_length=64, min_length=3)
    content: str = Field(min_length=2)
    category: int


# generate AdminCreateThreadSchema
class AdminCreateThreadSchema(AdminCreateCategorySchema):
    """Admin create thread schema."""

    author_id: int


class UpdateThreadSchema(BaseModel):
    """Update thread schema."""

    title: str | None = Field(max_length=64)
    content: str | None


# generate AdminUpdateThreadSchema
class AdminUpdateThreadSchema(UpdateThreadSchema):
    """Admin update thread schema."""

    author_id: int | None
    category_id: int | None


class CreatePostSchema(BaseModel):
    """Create post schema."""

    thread_id: int
    content: str = Field(min_length=2)


class UpdatePostSchema(BaseModel):
    """Update post schema."""

    content: str


class CreateCategorySchema(BaseModel):
    """Create category schema."""

    name: str
    description: str | None
    type: CategoryTypeEnum = CategoryTypeEnum.PUBLIC


class CreateThreadSchema(BaseModel):
    """Create thread schema."""

    title: str = Field(max_length=64, min_length=3)
    content: str = Field(min_length=2)
    category: int
    server_id: int | None = None
    question_experience: int | None = None
    question_age: int | None = None
    question_reason: int | None = None


class AdminCreatePostSchema(CreatePostSchema):
    """Admin create post schema."""

    user_id: int


class AdminUpdatePostSchema(UpdatePostSchema):
    """Admin update post schema."""

    user_id: int | None
    thread_id: int | None


class ThreadQuery(OrderQuery):
    """Thread query schema."""

    category: int | None = Query(None, description="Category ID", gt=0)
    server: int | None = Query(None, description="Server ID", gt=0)
    status: str | None = Query(
        None,
        description="Thread status",
        enum=ThreadStatusEnum,
    )
    closed: bool | None = Query(None, description="Is thread closed")


class PostQuery(OrderQuery):
    """Post query schema."""


class AdminThreadActionSchema(BaseModel):
    """Admin thread action schema."""

    action: ThreadActionEnum = ThreadActionEnum.CLOSE.value
    category: int | None = None
