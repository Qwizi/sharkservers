from fastapi import HTTPException
from starlette import status

from src.forum.enums import (
    CategoryExceptionEnum,
    TagExceptionEnum,
    ThreadExceptionEnum,
    PostExceptionsEnum,
    LikeExceptionsEnum,
)

category_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=CategoryExceptionEnum.NOT_FOUND,
)

tag_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=TagExceptionEnum.NOT_FOUND,
)
thread_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=ThreadExceptionEnum.NOT_FOUND,
)
thread_exists_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=ThreadExceptionEnum.ALREADY_EXISTS,
)
thread_is_closed_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail=ThreadExceptionEnum.IS_CLOSED
)

thread_not_valid_author_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=ThreadExceptionEnum.NOT_VALID_THREAD_AUTHOR,
)

post_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=PostExceptionsEnum.NOT_FOUND,
)

post_not_valid_author_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=PostExceptionsEnum.NOT_VALID_AUTHOR,
)

like_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=PostExceptionsEnum.NOT_FOUND,
)

like_already_exists_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=LikeExceptionsEnum.ALREADY_EXISTS,
)

thread_meta_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=ThreadExceptionEnum.NOT_FOUND,
)
