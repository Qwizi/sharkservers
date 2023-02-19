from typing import Optional, List

import ormar

from src.db import DateFieldsMixins, BaseMeta
from src.forum.enums import CategoryTypeEnum, ThreadStatusEnum
from src.servers.models import Server
from src.users.models import User


class SpecialThreadQuestion(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "forum_special_thread_questions"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=64, unique=True)
    value: str = ormar.String(max_length=256)


class Category(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "forum_categories"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=64, unique=True)
    description: str = ormar.Text(nullable=True)
    type: str = ormar.String(
        max_length=64,
        choices=list(CategoryTypeEnum),
        default=CategoryTypeEnum.PUBLIC.value,
    )
    special_thread_question: Optional[SpecialThreadQuestion] = ormar.ManyToMany(
        SpecialThreadQuestion,
        related_name="category_sp_thread_question",
        nullable=True,
    )


class Tag(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "forum_tags"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=64, unique=True)


class Post(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "forum_posts"

    id: int = ormar.Integer(primary_key=True)
    author: Optional[User] = ormar.ForeignKey(User, related_name="user_posts")
    content: str = ormar.Text()


class Thread(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "forum_threads"

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=64)
    content: str = ormar.Text()
    is_closed: bool = ormar.Boolean(default=False)
    status: Optional[str] = ormar.String(
        max_length=64, choices=list(ThreadStatusEnum), default=None, nullable=True
    )
    category: Optional[Category] = ormar.ForeignKey(Category)
    author: Optional[User] = ormar.ForeignKey(User, relaed_name="user_threads")
    posts: Optional[List[Post]] = ormar.ManyToMany(Post, related_name="thread_post")
    tags: Optional[List[Tag]] = ormar.ManyToMany(Tag, related_name="thread_tag")
    server: Optional[Server] = ormar.ForeignKey(
        Server, related_name="server_threads", nullable=True
    )
