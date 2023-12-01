from typing import *

from pydantic import BaseModel, Field

from .AuthTypeEnum import AuthTypeEnum


class UpdateAdminSchema(BaseModel):
    """
    UpdateAdminSchema model

    """

    authtype: Optional[AuthTypeEnum] = Field(alias="authtype", default=None)

    identity: Optional[str] = Field(alias="identity", default=None)

    password: Optional[str] = Field(alias="password", default=None)

    flags: Optional[str] = Field(alias="flags", default=None)

    name: Optional[str] = Field(alias="name", default=None)

    immunity: Optional[int] = Field(alias="immunity", default=None)

    groups_id: Optional[List[int]] = Field(alias="groups_id", default=None)
