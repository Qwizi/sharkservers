from typing import *

from pydantic import BaseModel, Field


class CreateGroupSchema(BaseModel):
    """
    CreateGroupSchema model

    """

    name: str = Field(alias="name")

    immunity_level: int = Field(alias="immunity_level")

    flags: Optional[str] = Field(alias="flags", default=None)
