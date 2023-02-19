from typing import Optional, List

import pydantic
from pydantic import BaseModel, Field

from src.forum.enums import CategoryTypeEnum
from src.forum.models import Category, Tag, Thread
from src.roles.models import Role

category_out = Category.get_pydantic()
tags_out = Tag.get_pydantic()
thread_out = Thread.get_pydantic(
    exclude={
        "author__password",
        "author__email",
        "author__display_role__scopes",
        "author__secret_salt",
        "author__roles",
    }
)


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


class ThreadOut(BaseModel):
    id: int
    title: str
    is_closed: bool
    content: str
    category: ThreadCategory
    author: ThreadAuthor
    tags: Optional[List[ThreadTag]] = None


class CreateThreadSchema(BaseModel):
    title: str = Field(max_length=64)
    content: str
    category: int
    # tags: Optional[List[str]] = None


# generate AdminCreateThreadSchema
class AdminCreateThreadSchema(CreateThreadSchema):
    author_id: int


class UpdateThreadSchema(BaseModel):
    title: Optional[str] = Field(max_length=64)
    content: Optional[str]


# generate AdminUpdateThreadSchema
class AdminUpdateThreadSchema(UpdateThreadSchema):
    author_id: Optional[int]
    category_id: Optional[int]


class PostOut(BaseModel):
    id: int
    content: str
    author: ThreadAuthor


class CreatePostSchema(BaseModel):
    thread_id: int
    content: str


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
