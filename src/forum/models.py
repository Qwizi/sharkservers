from typing import Optional, List

import ormar
from ormar import post_save, post_delete, post_relation_add, post_relation_remove

from src.db import DateFieldsMixins, BaseMeta
from src.forum.enums import CategoryTypeEnum, ThreadStatusEnum
from src.logger import logger
from src.servers.models import Server
from src.users.models import User


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
    threads_count: int = ormar.Integer(default=0)


class Tag(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "forum_tags"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=64, unique=True)


class Like(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "forum_reputation"

    id: int = ormar.Integer(primary_key=True)
    author: Optional[User] = ormar.ForeignKey(User, related_name="user_reputation")


class Post(ormar.Model, DateFieldsMixins):
    class Meta(BaseMeta):
        tablename = "forum_posts"

    id: int = ormar.Integer(primary_key=True)
    author: Optional[User] = ormar.ForeignKey(User, related_name="user_posts")
    content: str = ormar.Text()
    likes: Optional[List[Like]] = ormar.ManyToMany(Like, related_name="post_likes")
    likes_count = ormar.Integer(default=0)


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
    post_count: int = ormar.Integer(default=0)


@post_save(Thread)
async def update_category_thread_counter_after_save(sender, instance, **kwargs):
    category = await Category.objects.get(id=instance.category.id)
    await category.update(threads_count=category.threads_count + 1)


@post_delete(Thread)
async def update_category_thread_counter_after_delete(sender, instance, **kwargs):
    category = await Category.objects.get(id=instance.category.id)
    await category.update(threads_count=category.threads_count - 1 if category.threads_count > 0 else 0)


@post_relation_add(Thread)
async def update_thread_post_counter_after_relation_add(sender, instance, child, **kwargs):
    thread = await Thread.objects.get(id=instance.id)
    await thread.update(post_count=thread.post_count + 1)
    logger.info(f"Thread {thread.title} post count updated to {thread.post_count}")


@post_relation_remove(Thread)
async def update_thread_post_counter_after_relation_remove(sender, instance, child, **kwargs):
    thread = await Thread.objects.get(id=instance.id)
    await thread.update(post_count=thread.post_count - 1 if thread.post_count > 0 else 0)
    logger.info(f"Thread {thread.title} post count updated to {thread.post_count}")
