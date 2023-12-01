from typing import *

from pydantic import BaseModel, Field

from .AdminOut import AdminOut


class Page_AdminOut_(BaseModel):
    """
    Page[AdminOut] model

    """

    items: List[AdminOut] = Field(alias="items")

    total: int = Field(alias="total")

    page: Optional[int] = Field(alias="page", default=None)

    size: Optional[int] = Field(alias="size", default=None)

    pages: Optional[int] = Field(alias="pages", default=None)
