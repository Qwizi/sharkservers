from pydantic import BaseModel

from src.scopes.models import Scope

ScopeOut = Scope.get_pydantic(exclude={"roles"})


class CreateScopeSchema(BaseModel):
    app_name: str
    value: str
    description: str
    protected: bool = True
