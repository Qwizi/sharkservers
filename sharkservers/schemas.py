"""
Module contains the schema definitions used in the SharkServers API.

It includes the following classes:
- CreateAdmin: Represents the schema for creating an admin user.
- HTTPErrorSchema: Represents the base schema for HTTP error responses.
- HTTPError404Schema: Represents the schema for a 404 Not Found error response.
- HTTPError400Schema: Represents the schema for a 400 Bad Request error response.
- HTTPError401Schema: Represents the schema for a 401 Unauthorized error response.
- OrderQuery: Represents the schema for the order query parameter.
"""  # noqa: EXE002
from typing import Optional

from fastapi import Query
from pydantic import BaseModel
from starlette import status

from sharkservers.enums import OrderEnum


class CreateAdmin(BaseModel):
    """
    Represents the data required to create an admin.

    Attributes
    ----------
        admin_username (str): The username of the admin.
        admin_password (str): The password of the admin.
        admin_email (str): The email address of the admin.
    """

    admin_username: str
    admin_password: str
    admin_email: str


class HTTPErrorSchema(BaseModel):
    """
    Schema for representing an HTTP error response.

    Attributes
    ----------
        detail (str): The error message.
    """

    detail: str


class HTTPError404Schema(HTTPErrorSchema):
    """Schema for representing a 404 Not Found HTTP error."""

    status_code: int = status.HTTP_404_NOT_FOUND


class HTTPError400Schema(HTTPErrorSchema):
    """Schema for HTTP 400 Bad Request error."""

    status_code: int = status.HTTP_400_BAD_REQUEST


class HTTPError401Schema(HTTPErrorSchema):
    """
    Schema for representing a 401 Unauthorized HTTP error.

    Inherits from the base HTTPErrorSchema class.
    """

    status_code: int = status.HTTP_401_UNAUTHORIZED


class OrderQuery(BaseModel):
    """
    Represents the query parameters for ordering data.

    :param order_by: The field to order by.
    """

    order_by: Optional[str] = Query(
        OrderEnum.ID_DESC,
        description="Order by",
        enum=OrderEnum,
    )