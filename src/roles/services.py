from src.db import BaseService
from src.roles.exceptions import role_not_found_exception
from src.roles.models import Role


class RoleService(BaseService):
    pass


roles_service = RoleService(Role, not_found_exception=role_not_found_exception)
