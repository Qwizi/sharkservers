from typing import *

from pydantic import BaseModel, Field

from .AuthTypeEnum import AuthTypeEnum


class CreateAdminSchema(BaseModel):
    """
    CreateAdminSchema model

    """

    authtype: Optional[AuthTypeEnum] = Field(alias="authtype", default=None)

    identity: str = Field(alias="identity")

    password: Optional[str] = Field(alias="password", default=None)

    flags: Optional[str] = Field(alias="flags", default=None)

    name: str = Field(alias="name")

    immunity: int = Field(alias="immunity")

    groups_id: Optional[List[int]] = Field(alias="groups_id", default=None)
