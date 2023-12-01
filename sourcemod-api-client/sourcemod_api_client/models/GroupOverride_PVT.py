from typing import *

from pydantic import BaseModel, Field


class GroupOverride_PVT(BaseModel):
    """
    GroupOverride_PVT model

    """

    id: Optional[int] = Field(alias="id", default=None)

    type: Optional[str] = Field(alias="type", default=None)

    name: str = Field(alias="name")

    access: Optional[str] = Field(alias="access", default=None)
