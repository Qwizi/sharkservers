"""Players exceptions."""  # noqa: EXE002
from fastapi import HTTPException
from starlette import status

player_not_found_exception = HTTPException(
    detail="Player not found",
    status_code=status.HTTP_404_NOT_FOUND,
)

player_server_stats_not_found_exception = HTTPException(
    detail="Player server stats not found",
    status_code=status.HTTP_404_NOT_FOUND,
)
