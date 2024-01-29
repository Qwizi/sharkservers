"""Exception handlers for FastAPI."""
from __future__ import annotations

import sys
from typing import Union

from fastapi import Request
from fastapi.exception_handlers import http_exception_handler as _http_exception_handler
from fastapi.exception_handlers import (
    request_validation_exception_handler as _request_validation_exception_handler,
)
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse, Response

from sharkservers.logger import logger


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Middleware will log all RequestValidationErrors.

    Args:
    ----
        request: The request object.
        exc: The RequestValidationError exception.

    Returns:
    -------
        A JSONResponse with the errors and the request body.

    """
    logger.debug("Our custom request_validation_exception_handler was called")
    body = await request.body()
    query_params = request.query_params._dict  # pylint: disable=protected-access
    detail = {
        "errors": exc.errors(),
        "body": body.decode(),
        "query_params": query_params,
    }
    logger.info(detail)
    return await _request_validation_exception_handler(request, exc)


async def http_exception_handler(
    request: Request, exc: HTTPException
) -> Union[JSONResponse, Response]:
    """
    HTTPException handler.

    Args:
    ----
        request: The request object.
        exc: The HTTPException exception.

    Returns:
    -------
        A JSONResponse with the error.
    """
    logger.error(f"{exc.detail} <{exc.detail.value}>")
    return await _http_exception_handler(request, exc)


async def unhandled_exception_handler(
    request: Request, exc: Exception
) -> PlainTextResponse:
    """
    Unhandled exception handler.

    Args:
    ----
        request: The request object.
        exc: The exception.

    Returns:
    -------
        A PlainTextResponse with the error.
    """
    logger.debug("Our custom unhandled_exception_handler was called")
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    url = (
        f"{request.url.path}?{request.query_params}"
        if request.query_params
        else request.url.path
    )
    exception_type, exception_value, exception_traceback = sys.exc_info()
    exception_name = getattr(exception_type, "__name__", None)
    logger.error(
        f'{host}:{port} - "{request.method} {url}" 500 Internal Server Error <{exception_name}: {exception_value}>',
    )
    return PlainTextResponse(str(exc), status_code=500)
