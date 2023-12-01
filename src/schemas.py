from typing import Optional
from fastapi import Query
from pydantic import BaseModel
from starlette import status

from src.enums import OrderEnum


class CreateAdmin(BaseModel):
    admin_username: str
    admin_password: str
    admin_email: str


class HTTPErrorSchema(BaseModel):
    detail: str


class HTTPError404Schema(HTTPErrorSchema):
    status_code: int = status.HTTP_404_NOT_FOUND


class HTTPError400Schema(HTTPErrorSchema):
    status_code: int = status.HTTP_400_BAD_REQUEST


class HTTPError401Schema(HTTPErrorSchema):
    status_code: int = status.HTTP_401_UNAUTHORIZED


class OrderQuery(BaseModel):
    order_by: Optional[str] = Query(
        OrderEnum.ID_DESC, description="Order by", enum=OrderEnum
    )
