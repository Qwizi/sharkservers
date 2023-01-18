from fastapi import HTTPException
from starlette import status

from src.forum.enums import CategoriesExceptionsEnum, TagsExceptionsEnum, ThreadsExceptionsEnum, \
    PostsExceptionsEnum

category_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=CategoriesExceptionsEnum.NOT_FOUND,
)

tag_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=TagsExceptionsEnum.NOT_FOUND,
)
thread_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=ThreadsExceptionsEnum.NOT_FOUND,
)
thread_exists_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=ThreadsExceptionsEnum.ALREADY_EXISTS,
)
thread_is_closed_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=ThreadsExceptionsEnum.IS_CLOSED
)

post_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=PostsExceptionsEnum.NOT_FOUND,
)
