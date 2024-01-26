# apps schemas
from typing import Optional

from pydantic import BaseModel

from sharkservers.apps.models import App

AppsOut = App.get_pydantic()


class CreateAppSchema(BaseModel):
    name: str
    description: str
    scopes: Optional[list[int]]


class UpdateAppsSchema(BaseModel):
    pass
