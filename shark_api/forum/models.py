from typing import Optional, List

import ormar

from shark_api.db import DateFieldsMixins, BaseMeta
from shark_api.users.models import User


class Category(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "forum_categories"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=64, unique=True)


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
    category: Optional[Category] = ormar.ForeignKey(Category)
    author: Optional[User] = ormar.ForeignKey(User, relaed_name="user_threads")
    posts: Optional[List[Post]] = ormar.ManyToMany(Post, related_name="thread_post")
    tags: Optional[List[Tag]] = ormar.ManyToMany(Tag, related_name="thread_tag")
