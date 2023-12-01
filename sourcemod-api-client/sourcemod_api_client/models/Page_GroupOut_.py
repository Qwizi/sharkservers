from typing import *

from pydantic import BaseModel, Field

from .GroupOut import GroupOut


class Page_GroupOut_(BaseModel):
    """
    Page[GroupOut] model

    """

    items: List[GroupOut] = Field(alias="items")

    total: int = Field(alias="total")

    page: Optional[int] = Field(alias="page", default=None)

    size: Optional[int] = Field(alias="size", default=None)

    pages: Optional[int] = Field(alias="pages", default=None)
