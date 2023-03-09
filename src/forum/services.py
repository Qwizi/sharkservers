from src.db import BaseService
from src.forum.exceptions import (
    category_not_found_exception,
    thread_not_found_exception,
    post_not_found_exception,
)
from src.forum.models import Category, Thread, Post


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


class PostService(BaseService):
    class Meta:
        model = Post
        not_found_exception = post_not_found_exception


class SpecialThreadQuestionService(BaseService):
    pass
