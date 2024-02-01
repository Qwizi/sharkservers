"""Forum models."""
from __future__ import annotations

import uuid

import ormar
from ormar import post_delete, post_relation_add, post_relation_remove, post_save

from sharkservers.db import BaseMeta, DateFieldsMixins
from sharkservers.forum.enums import (
    CategoryTypeEnum,
    ThreadActionEnum,
    ThreadStatusEnum,
)
from sharkservers.logger import logger
from sharkservers.servers.models import Server
from sharkservers.users.models import User


class Category(ormar.Model, DateFieldsMixins):
    """
    Category model.

    Attributes
    ----------
        id (int): Category ID
        name (str): Category name
        description (str): Category description
        type (str): Category type
        threads_count (int): Category threads count
    """

    class Meta(BaseMeta):
        """Meta class for Category model."""

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


class Like(ormar.Model, DateFieldsMixins):
    """
    Like model.

    Attributes
    ----------
        id (int): Like ID
        author (User): Like author
    """

    class Meta(BaseMeta):
        """Meta class for Like model."""

        tablename = "forum_reputation"

    id: int = ormar.Integer(primary_key=True)
    author: User | None = ormar.ForeignKey(User, related_name="user_reputation")


class Post(ormar.Model, DateFieldsMixins):
    """
    Post model.

    Attributes
    ----------
        id (int): Post ID
        author (User): Post author
        content (str): Post content
        likes (List[Like]): Post likes
        likes_count (int): Post likes count
    """

    class Meta(BaseMeta):
        """Meta class for Post model."""

        tablename = "forum_posts"

    id: int = ormar.Integer(primary_key=True)
    author: User | None = ormar.ForeignKey(User, related_name="user_posts")
    content: str = ormar.Text()
    likes: list[Like] | None = ormar.ManyToMany(Like, related_name="post_likes")
    likes_count = ormar.Integer(default=0)


class ThreadMeta(ormar.Model, DateFieldsMixins):
    """
    Thread meta model.

    Attributes
    ----------
        id (str): Thread meta ID
        name (str): Thread meta name
        value (str): Thread meta value
        description (str): Thread meta description
    """

    class Meta(BaseMeta):
        """Meta class for ThreadMeta model."""

        tablename = "forum_threads_meta"

    id: str = ormar.UUID(primary_key=True, default=uuid.uuid4)
    name: str | None = ormar.String(max_length=64)
    value: str | None = ormar.Text(nullable=True)
    description: str | None = ormar.Text(nullable=True)


class Thread(ormar.Model, DateFieldsMixins):
    """
    Thread model.

    Attributes
    ----------
        id (int): Thread ID
        title (str): Thread title
        content (str): Thread content
        is_closed (bool): Is thread closed
        is_pinned (bool): Is thread pinned
        status (str): Thread status
        category (Category): Thread category
        author (User): Thread author
        posts (List[Post]): Thread posts
        meta_fields (List[ThreadMeta]): Thread meta fields
        post_count (int): Thread post count
    """

    class Meta(BaseMeta):
        """Meta class for Thread model."""

        tablename = "forum_threads"

    id: int = ormar.Integer(primary_key=True)
    title: str | None = ormar.String(max_length=64)
    content: str | None = ormar.Text()
    is_closed: bool | None = ormar.Boolean(default=False)
    is_pinned: bool | None = ormar.Boolean(default=False)
    status: str | None = ormar.String(
        max_length=64,
        choices=list(ThreadStatusEnum),
        default=None,
        nullable=True,
    )
    category: Category | None = ormar.ForeignKey(Category)
    author: User | None = ormar.ForeignKey(User, related_name="user_threads")
    posts: list[Post] | None = ormar.ManyToMany(Post, related_name="thread_post")
    meta_fields: list[ThreadMeta] | None = ormar.ManyToMany(
        ThreadMeta,
        related_name="thread_meta",
    )
    post_count: int = ormar.Integer(default=0)
    server: Server | None = ormar.ForeignKey(Server, related_name="thread_server")

    async def close(self) -> None:
        """Close thread."""
        await self.update(is_closed=True)

    async def open(self) -> None:
        """Open thread."""
        await self.update(is_closed=False)

    async def approve(self) -> None:
        """Approve thread."""
        await self.update(status=ThreadStatusEnum.APPROVED)
        await self.close()

    async def reject(self) -> None:
        """Reject thread."""
        await self.update(status=ThreadStatusEnum.REJECTED)
        await self.close()

    async def pin(self) -> None:
        """Pin thread."""
        await self.update(is_pinned=True)

    async def unpin(self) -> None:
        """Unpin thread."""
        await self.update(is_pinned=False)

    async def change_category(self, new_category: Category) -> None:
        """Change thread category."""
        await self.update(category=new_category)

    async def run_action(
        self,
        action: ThreadActionEnum,
        new_category: Category = None,
    ) -> None:
        """Run thread action."""
        if action == ThreadActionEnum.APPROVE:
            await self.approve()
        elif action == ThreadActionEnum.REJECT:
            await self.reject()
        elif action == ThreadActionEnum.PIN:
            await self.pin()
        elif action == ThreadActionEnum.UNPIN:
            await self.unpin()
        elif action == ThreadActionEnum.MOVE:
            await self.change_category(new_category=new_category)
        elif action == ThreadActionEnum.CLOSE:
            await self.close()
        elif action == ThreadActionEnum.OPEN:
            await self.open()


@post_save(Thread)
async def on_thread_save(
    sender, instance, **kwargs
) -> None:  # noqa: ANN003, ARG001, ANN001
    """
    On thread save event.

    Args:
    ----
        sender (Thread): Thread model
        instance (Thread): Thread instance
        **kwargs: Additional arguments

    Returns:
    -------
        None
    """
    # Update category thread counter
    category = await Category.objects.get(id=instance.category.id)
    threads_category_count = category.threads_count + 1
    threads_count = instance.author.threads_count + 1
    await category.update(threads_count=threads_category_count)
    await instance.author.update(threads_count=threads_count)
    # Check category type
    if category.type == CategoryTypeEnum.APPLICATION:
        # create thread server_id meta field
        server_id = await ThreadMeta.objects.create(
            name="server_id",
            description="Serwer na który aplikujesz",
        )
        experience = await ThreadMeta.objects.create(
            name="question_experience",
            description="Twoje doświadczenie",
        )
        age = await ThreadMeta.objects.create(
            name="question_age",
            description="Twój wiek",
        )
        reason = await ThreadMeta.objects.create(
            name="question_reason",
            description="Dlaczego chcesz zostac administratorem?",
        )
        meta_fields = [
            server_id,
            experience,
            age,
            reason,
        ]
        for meta_field in meta_fields:
            await instance.meta_fields.add(meta_field)


@post_delete(Thread)
async def update_category_thread_counter_after_delete(
    sender: Thread,  # noqa: ARG001
    instance: Thread,
    **kwargs,  # noqa: ARG001, ANN003
) -> None:
    """
    Update category thread counter after thread delete.

    Args:
    ----
        sender (Thread): Thread model
        instance (Thread): Thread instance
        **kwargs: Additional arguments
    """
    category = await Category.objects.get(id=instance.category.id)
    await category.update(
        threads_count=category.threads_count - 1 if category.threads_count > 0 else 0,
    )


@post_relation_add(Thread)
async def update_thread_post_counter_after_relation_add(
    sender: Thread,  # noqa: ARG001
    instance: Thread,
    child: Post,
    **kwargs,  # noqa: ARG001, ANN003
) -> None:
    """Update thread post counter after relation add."""
    if isinstance(child, Post):
        thread = await Thread.objects.get(id=instance.id)
        thread_posts_count = thread.post_count + 1
        posts_count = child.author.posts_count + 1
        await thread.update(post_count=thread_posts_count)
        logger.info(f"Thread {thread.title} post count updated to {thread.post_count}")
        await child.author.update(posts_count=posts_count)


@post_relation_remove(Thread)
async def update_thread_post_counter_after_relation_remove(
    sender: Thread,  # noqa: ARG001
    instance: Thread,
    child: Post,
    **kwargs,  # noqa: ANN003, ARG001
) -> None:
    """Update thread post counter after relation remove."""
    if isinstance(child, Post):
        thread = await Thread.objects.get(id=instance.id)
        thread_posts_count = thread.post_count - 1 if thread.post_count > 0 else 0
        posts_count = (
            child.author.posts_count - 1 if child.author.posts_count > 0 else 0
        )
        await thread.update(post_count=thread_posts_count)
        logger.info(f"Thread {thread.title} post count updated to {thread.post_count}")
        await child.author.update(posts_count=posts_count)
