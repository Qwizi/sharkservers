from typing import Optional, List

import pydantic
from pydantic import BaseModel, Field

from shark_api.forum.models import Category, Tag, Thread
from shark_api.roles.models import Role

category_out = Category.get_pydantic()
tags_out = Tag.get_pydantic()
thread_out = Thread.get_pydantic(
    exclude={"author__password", "author__email", "author__display_role__scopes", "author__secret_salt",
             "author__roles"})


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


class ThreadPost(BaseModel):
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


class CreateThread(BaseModel):
    title: str = Field(max_length=64)
    content: str
    category: int
    # tags: Optional[List[str]] = None


class UpdateThreadSchema(BaseModel):
    title: Optional[str] = Field(max_length=64)
    content: Optional[str]
    category: Optional[int]
    is_closed: Optional[bool]


class PostOut(BaseModel):
    id: int
    content: str
    author: ThreadAuthor


class CreatePost(BaseModel):
    thread_id: int
    content: str


class CreateCategorySchema(BaseModel):
    name: str
