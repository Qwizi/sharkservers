from typing import Optional

from pydantic import BaseModel, Field

from src.forum.enums import CategoryTypeEnum
from src.forum.models import Category, Tag, Thread, Post, Like
from src.roles.models import Role

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
}

category_out = Category.get_pydantic(exclude={"threads"})
tags_out = Tag.get_pydantic()
thread_out = Thread.get_pydantic(
    exclude=author_exclude | {"posts", "server", "tags"},
)
post_out = Post.get_pydantic(exclude=author_exclude | {"likes", "thread_post"})
like_out = Like.get_pydantic(exclude=author_exclude | {"post_likes"})


class CategoryOut(category_out):
    pass


class ThreadOut(thread_out):
    pass


class PostOut(post_out):
    pass


class LikeOut(like_out):
    pass


class ThreadTag(BaseModel):
    id: int
    name: str


class ThreadCategory(BaseModel):
    id: int
    name: str


class ThreadAuthor(BaseModel):
    id: int
    username: str
    avatar: str
    display_role: Role


class ThreadPostSchema(BaseModel):
    id: int
    content: str
    author: ThreadAuthor


class AdminCreateCategorySchema(BaseModel):
    title: str = Field(max_length=64, min_length=3)
    content: str = Field(min_length=2)
    category: int
    # tags: Optional[List[str]] = None


# generate AdminCreateThreadSchema
class AdminCreateThreadSchema(AdminCreateCategorySchema):
    author_id: int


class UpdateThreadSchema(BaseModel):
    title: Optional[str] = Field(max_length=64)
    content: Optional[str]


# generate AdminUpdateThreadSchema
class AdminUpdateThreadSchema(UpdateThreadSchema):
    author_id: Optional[int]
    category_id: Optional[int]


class CreatePostSchema(BaseModel):
    thread_id: int
    content: str = Field(min_length=2)


class UpdatePostSchema(BaseModel):
    content: str


class CreateCategorySchema(BaseModel):
    name: str
    description: Optional[str]
    type: CategoryTypeEnum = CategoryTypeEnum.PUBLIC


class AdminCreatePostSchema(CreatePostSchema):
    user_id: int


class AdminUpdatePostSchema(UpdatePostSchema):
    user_id: Optional[int]
    thread_id: Optional[int]