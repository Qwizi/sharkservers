from fastapi import HTTPException
from starlette import status as starlette_status
from src.roles.enums import ProtectedDefaultRolesTagEnum
from src.db import BaseService
from src.forum.enums import ThreadStatusEnum, ThreadActionEnum, CategoryTypeEnum
from src.forum.exceptions import (
    category_not_found_exception,
    thread_not_found_exception,
    post_not_found_exception,
    like_not_found_exception,
    like_already_exists_exception,
    thread_meta_not_found_exception,
)
from src.forum.models import Category, Thread, Post, Like, ThreadMeta
from src.forum.schemas import CreateThreadSchema
from src.servers.services import ServerService
from src.users.models import User
from src.logger import logger


class CategoryService(BaseService):
    class Meta:
        model = Category
        not_found_exception = category_not_found_exception

    async def sync_counters(self):
        try:
            categories = await self.Meta.model.objects.select_related("threads").all()
            for category in categories:
                threads_count = await category.threads.count()
                await category.update(threads_count=threads_count)
            logger.info(
                f"Finished sync counters to category threads -> {len(categories)}"
            )
        except Exception as e:
            logger.error(e)


class ThreadMetaService(BaseService):
    class Meta:
        model = ThreadMeta
        not_found_exception = thread_meta_not_found_exception

    async def fill_meta(self, thread_id: int, data: dict):
        for key, value in data.items():
            thread_meta = await self.get_one(name=key, thread_meta__id=thread_id)
            await thread_meta.update(value=value)


class ThreadService(BaseService):
    class Meta:
        model = Thread
        not_found_exception = thread_not_found_exception

    @staticmethod
    async def close_thread(thread: Thread):
        await thread.update(is_closed=True)
        return thread

    @staticmethod
    async def open_thread(thread: Thread):
        await thread.update(is_closed=False)
        return thread

    @staticmethod
    async def change_status(thread: Thread, status: ThreadStatusEnum):
        await thread.update(status=status)
        return thread

    async def approve(self, thread: Thread):
        await self.set_author_role(thread)
        await self.change_status(thread, ThreadStatusEnum.APPROVED)
        await self.close_thread(thread)
        return thread

    async def reject(self, thread: Thread):
        await self.change_status(thread, ThreadStatusEnum.REJECTED)
        await self.close_thread(thread)
        return thread

    @staticmethod
    async def pin_thread(thread: Thread):
        await thread.update(is_pinned=True)
        return thread

    @staticmethod
    async def unpin_thread(thread: Thread):
        await thread.update(is_pinned=False)
        return thread

    @staticmethod
    async def change_category(thread: Thread, new_category: Category):
        await thread.update(category=new_category)
        return thread

    async def run_action(
        self, thread: Thread, action: ThreadActionEnum, new_category: Category = None
    ):
        if action == ThreadActionEnum.APPROVE:
            return await self.approve(thread)
        elif action == ThreadActionEnum.REJECT:
            return await self.reject(thread)
        elif action == ThreadActionEnum.CLOSE:
            return await self.close_thread(thread)
        elif action == ThreadActionEnum.OPEN:
            return await self.open_thread(thread)
        elif action == ThreadActionEnum.PIN:
            return await self.pin_thread(thread)
        elif action == ThreadActionEnum.UNPIN:
            return await self.unpin_thread(thread)
        elif action == ThreadActionEnum.MOVE:
            return await self.change_category(thread, new_category)

    async def create_thread(
        self,
        data: CreateThreadSchema,
        author: User,
        category: Category,
        status: ThreadStatusEnum = ThreadStatusEnum.PENDING.value,
        thread_meta_service: ThreadMetaService = None,
        servers_service: ServerService = None,
        **kwargs,
    ):
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
                ],
            )
        new_thread = await self.create(
            title=data.title,
            content=data.content,
            category=category,
            author=author,
            status=status,
            **kwargs,
        )
        return new_thread

    async def sync_counters(self):
        try:
            threads = await self.Meta.model.objects.select_related("posts").all()
            for thread in threads:
                posts_count = await thread.posts.count()
                await thread.update(post_count=posts_count)
            logger.info(f"Finished sync counters to thread posts -> {len(threads)}")
        except Exception as e:
            logger.error(e)

    async def set_author_role(self, thread: Thread):
        user = thread.author
        admin_role = thread.server.admin_role
        if user.display_role.tag == ProtectedDefaultRolesTagEnum.USER.value:
            await user.update(display_role=admin_role)
            await user.roles.add(admin_role)
        else:
            await user.roles.add(admin_role)


class PostService(BaseService):
    class Meta:
        model = Post
        not_found_exception = post_not_found_exception

    async def sync_counters(self):
        try:
            posts = await self.Meta.model.objects.select_related("likes").all()
            for post in posts:
                likes_count = await post.likes.count()
                await post.update(likes_count=likes_count)
            logger.info(f"Finished sync counters to post likes -> {len(posts)}")
        except Exception as e:
            logger.error(e)


class SpecialThreadQuestionService(BaseService):
    pass


class LikeService(BaseService):
    class Meta:
        model = Like
        not_found_exception = like_not_found_exception

    async def add_like_to_post(self, post: Post, author: User):
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

    async def remove_like_from_post(self, post: Post, author: User):
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
