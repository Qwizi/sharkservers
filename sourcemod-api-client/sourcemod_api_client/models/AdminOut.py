from typing import *

from pydantic import BaseModel, Field

from .Group_WLC import Group_WLC


class AdminOut(BaseModel):
    """
    AdminOut model

    """

    created_at: Optional[str] = Field(alias="created_at", default=None)

    updated_at: Optional[str] = Field(alias="updated_at", default=None)

    id: Optional[int] = Field(alias="id", default=None)

    authtype: Optional[str] = Field(alias="authtype", default=None)

    identity: str = Field(alias="identity")

    password: Optional[str] = Field(alias="password", default=None)

    flags: str = Field(alias="flags")

    name: str = Field(alias="name")

    immunity: int = Field(alias="immunity")

    groups: Optional[List[Optional[Group_WLC]]] = Field(alias="groups", default=None)
