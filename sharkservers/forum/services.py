"""Forum services."""
from __future__ import annotations

from fastapi import HTTPException
from starlette import status as starlette_status

from sharkservers.db import BaseService
from sharkservers.forum.enums import (
    CategoryTypeEnum,
    ThreadStatusEnum,
)
from sharkservers.forum.exceptions import (
    category_not_found_exception,
    like_already_exists_exception,
    like_not_found_exception,
    post_not_found_exception,
    thread_meta_not_found_exception,
    thread_not_found_exception,
)
from sharkservers.forum.models import Category, Like, Post, Thread, ThreadMeta
from sharkservers.forum.schemas import CreateThreadSchema, LikeOut, ThreadOut
from sharkservers.logger import logger
from sharkservers.roles.enums import ProtectedDefaultRolesTagEnum
from sharkservers.servers.services import ServerService
from sharkservers.users.models import User


class CategoryService(BaseService):
    """Category service."""

    class Meta:
        """Category service meta."""

        model = Category
        not_found_exception = category_not_found_exception

    async def sync_counters(self) -> None:
        """Sync category threads counters."""
        try:
            categories = await self.Meta.model.objects.select_related("threads").all()
            for category in categories:
                threads_count = await category.threads.count()
                await category.update(threads_count=threads_count)
            logger.info(
                f"Finished sync counters to category threads -> {len(categories)}",
            )
        except Exception as e:  # noqa: BLE001
            logger.error(e)


class ThreadMetaService(BaseService):
    """Thread meta service."""

    class Meta:
        """Thread meta service meta."""

        model = ThreadMeta
        not_found_exception = thread_meta_not_found_exception

    async def fill_meta(self, thread_id: int, data: dict) -> ThreadMeta:
        """
        Fill thread meta.

        Args:
        ----
            thread_id (int): The thread id.
            data (dict): The data.

        Returns:
        -------
            ThreadMeta: The thread meta.
        """
        for key, value in data.items():
            thread_meta = await self.get_one(name=key, thread_meta__id=thread_id)
            await thread_meta.update(value=value)


class ThreadService(BaseService):
    """Thread service."""

    class Meta:
        """Thread service meta."""

        model = Thread
        not_found_exception = thread_not_found_exception

    async def create_thread(  # noqa: PLR0913
        self,
        data: CreateThreadSchema,
        author: User,
        category: Category,
        status: ThreadStatusEnum = ThreadStatusEnum.PENDING.value,
        thread_meta_service: ThreadMetaService = None,
        servers_service: ServerService = None,
        **kwargs,  # noqa: ANN003
    ) -> ThreadOut:
        """
        Create thread.

        Args:
        ----
            data (CreateThreadSchema): The data.
            author (User): The author.
            category (Category): The category.
            status (ThreadStatusEnum, optional): The status. Defaults to ThreadStatusEnum.PENDING.value.
            thread_meta_service (ThreadMetaService, optional): The thread meta service. Defaults to None.
            servers_service (ServerService, optional): The servers service. Defaults to None.
            **kwargs: The kwargs.

        Raises:
        ------
            HTTPException: The HTTP exception.

        Returns:
        -------
            ThreadOut: The thread.
        """
        if category.type == CategoryTypeEnum.APPLICATION:
            if not data.server_id:
                raise HTTPException(
                    status_code=starlette_status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="server_id is required",
                )
            if not data.question_experience:
                raise HTTPException(
                    status_code=starlette_status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="question_experience is required",
                )
            if not data.question_age:
                raise HTTPException(
                    status_code=starlette_status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="question_age is required",
                )
            if not data.question_reason:
                raise HTTPException(
                    status_code=starlette_status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="question_reason is required",
                )
            server = await servers_service.get_one(id=data.server_id)
            new_thread = await self.create(
                title=data.title,
                content=data.content,
                category=category,
                author=author,
                status=status,
                server=server,
                **kwargs,
            )
            await thread_meta_service.fill_meta(
                thread_id=new_thread.id,
                data={
                    "server_id": data.server_id,
                    "question_experience": data.question_experience,
                    "question_age": data.question_age,
                    "question_reason": data.question_reason,
                },
            )

            return await self.get_one(
                id=new_thread.id,
                related=[
                    "category",
                    "author",
                    "author__display_role",
                    "meta_fields",
                    "server",
                    "server__admin_role",
                    "author__player",
                    "author__player__steamrep_profile",
                ],
            )
        return await self.create(
            title=data.title,
            content=data.content,
            category=category,
            author=author,
            status=status,
            **kwargs,
        )

    async def sync_counters(self) -> None:
        """Sync thread posts counters."""
        try:
            threads = await self.Meta.model.objects.select_related("posts").all()
            for thread in threads:
                posts_count = await thread.posts.count()
                await thread.update(post_count=posts_count)
            logger.info(f"Finished sync counters to thread posts -> {len(threads)}")
        except Exception as e:  # noqa: BLE001
            logger.error(e)

    async def set_author_role(self, thread: Thread) -> None:
        """
        Set author role.

        Args:
        ----
            thread (Thread): The thread.

        Returns:
        -------
            None: None.
        """
        user = thread.author
        admin_role = thread.server.admin_role
        if user.display_role.tag == ProtectedDefaultRolesTagEnum.USER.value:
            await user.update(display_role=admin_role)
            await user.roles.add(admin_role)
        else:
            await user.roles.add(admin_role)


class PostService(BaseService):
    """Post service."""

    class Meta:
        """Post service meta."""

        model = Post
        not_found_exception = post_not_found_exception

    async def sync_counters(self) -> None:
        """Sync post likes counters."""
        try:
            posts = await self.Meta.model.objects.select_related("likes").all()
            for post in posts:
                likes_count = await post.likes.count()
                await post.update(likes_count=likes_count)
            logger.info(f"Finished sync counters to post likes -> {len(posts)}")
        except Exception as e:  # noqa: BLE001
            logger.error(e)


class LikeService(BaseService):
    """Like service."""

    class Meta:
        """Like service meta."""

        model = Like
        not_found_exception = like_not_found_exception

    async def add_like_to_post(self, post: Post, author: User) -> tuple[LikeOut, int]:
        """
        Add like to post.

        Args:
        ----
            post (Post): The post.
            author (User): The author.

        Raises:
        ------
            like_already_exists_exception: The like already exists exception.

        Returns:
        -------
            tuple[LikeOut, int]: The like and likes count.
        """
        like_exists = False
        for like in post.likes:
            if like.user == author:
                like_exists = True
                break
        if like_exists:
            raise like_already_exists_exception
        new_like = await self.create(author=author)
        await post.likes.add(new_like)
        return new_like, post.likes

    async def remove_like_from_post(self, post: Post, author: User) -> dict:
        """
        Remove like from post.

        Args:
        ----
            post (Post): The post.
            author (User): The author.

        Raises:
        ------
            like_not_found_exception: The like not found exception.

        Returns:
        -------
            dict: The dict.
        """
        like_exists = False
        for like in post.likes:
            if like.author == author:
                like_exists = True
                await post.likes.remove(like)
                await self.delete(_id=like.id)
                break
        if not like_exists:
            raise like_not_found_exception
        return {"message": "Like removed"}
