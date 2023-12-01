from typing import Optional

from pydantic import BaseModel

from src.scopes.models import Scope

ScopeOut = Scope.get_pydantic(exclude={"roles"})


class CreateScopeSchema(BaseModel):
    app_name: str
    value: str
    description: str
    protected: bool = True


class UpdateScopeSchema(BaseModel):
    app_name: Optional[str]
    value: Optional[str]
    description: Optional[str]
    protected: Optional[bool]
