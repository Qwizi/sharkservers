from typing import *

from pydantic import BaseModel, Field

from .GroupOverride_PVT import GroupOverride_PVT


class Group_WLC(BaseModel):
    """
    Group_WLC model

    """

    created_at: Optional[str] = Field(alias="created_at", default=None)

    updated_at: Optional[str] = Field(alias="updated_at", default=None)

    id: Optional[int] = Field(alias="id", default=None)

    flags: str = Field(alias="flags")

    name: str = Field(alias="name")

    immunity_level: int = Field(alias="immunity_level")

    groupoverrides: Optional[List[Optional[GroupOverride_PVT]]] = Field(alias="groupoverrides", default=None)
