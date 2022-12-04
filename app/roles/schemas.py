from app.roles.models import Role

RoleOut = Role.get_pydantic(exclude={"roles"})
RoleOutWithScopes = Role.get_pydantic()
