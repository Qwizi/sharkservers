from app.scopes.models import Scope

ScopeOut = Scope.get_pydantic(exclude={"roles"})
