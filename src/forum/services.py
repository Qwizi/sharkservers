from src.db import BaseService
from src.forum.exceptions import category_not_found_exception, thread_not_found_exception, post_not_found_exception
from src.forum.models import Category, Thread, Post
from src.forum.schemas import CreateThreadSchema


class CategoryService(BaseService):
    pass


class ThreadService(BaseService):

    @staticmethod
    async def close_thread(thread: Thread):
        await thread.update(is_closed=True)
        return thread

    @staticmethod
    async def open_thread(thread: Thread):
        await thread.update(is_closed=False)
        return thread


class PostService(BaseService):
    pass


categories_service = CategoryService(model=Category, not_found_exception=category_not_found_exception)
threads_service = ThreadService(model=Thread, not_found_exception=thread_not_found_exception)
posts_service = PostService(model=Post, not_found_exception=post_not_found_exception)
