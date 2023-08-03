from src.db import BaseService
from src.forum.enums import ThreadStatusEnum, ThreadActionEnum
from src.forum.exceptions import (category_not_found_exception, thread_not_found_exception, post_not_found_exception,
                                  like_not_found_exception, like_already_exists_exception,
                                  thread_meta_not_found_exception, )
from src.forum.models import Category, Thread, Post, Like, ThreadMeta
from src.users.models import User


class CategoryService(BaseService):
    class Meta:
        model = Category
        not_found_exception = category_not_found_exception


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
        await self.change_status(thread, ThreadStatusEnum.APPROVED)
        await self.close_thread(thread)
        return thread

    async def reject(self, thread: Thread):
        await self.change_status(thread, ThreadStatusEnum.REJECTED)
        await self.close_thread(thread)
        return thread

    async def run_action(self, thread: Thread, action: ThreadActionEnum):
        if action == ThreadActionEnum.APPROVE:
            return await self.approve(thread)
        elif action == ThreadActionEnum.REJECT:
            return await self.reject(thread)
        elif action == ThreadActionEnum.CLOSE:
            return await self.close_thread(thread)
        elif action == ThreadActionEnum.OPEN:
            return await self.open_thread(thread)


class PostService(BaseService):
    class Meta:
        model = Post
        not_found_exception = post_not_found_exception


class SpecialThreadQuestionService(BaseService):
    pass


class LikeService(BaseService):
    class Meta:
        model = Like
        not_found_exception = like_not_found_exception

    async def add_like_to_post(self, post: Post, user: User):
        like_exists = False
        for like in post.likes:
            if like.user == user:
                like_exists = True
                break
        if like_exists:
            raise like_already_exists_exception
        new_like = await self.create(user=user)
        await post.likes.add(new_like)
        return new_like, post.likes

    async def remove_like_from_post(self, post: Post, user: User):
        like_exists = False
        for like in post.likes:
            if like.user == user:
                like_exists = True
                await post.likes.remove(like)
                await self.delete(_id=like.id)
                break
        if not like_exists:
            raise like_not_found_exception
        return {"message": "Like removed"}


class ThreadMetaService(BaseService):
    class Meta:
        model = ThreadMeta
        not_found_exception = thread_meta_not_found_exception
