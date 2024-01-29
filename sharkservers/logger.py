"""Logging configuration for the server."""
import logging

# Disable uvicorn access logger
uvicorn_access = logging.getLogger("uvicorn.access")
uvicorn_access.disabled = True

logger = logging.getLogger("uvicorn")

logger.setLevel(logging.getLevelName(logging.DEBUG))


def logger_with_filename(filename: str, data: str) -> None:
    """
    Log a message with the filename and data.

    Args:
    ----
        filename (str): The filename to log.
        data (str): The data to log.

    Returns:
    -------
        None
    """
    logger.debug(f"{filename} | {data!s}")  # noqa: G004
