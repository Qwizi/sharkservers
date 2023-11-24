import ormar

from src.db import BaseMeta


class Scope(ormar.Model):
    class Meta(BaseMeta):
        tablename = "scopes"

    id = ormar.Integer(primary_key=True)
    app_name = ormar.String(max_length=64)
    value = ormar.String(max_length=120)
    description = ormar.String(max_length=256)
    protected = ormar.Boolean(default=True)

    def get_string(self):
        return f"{self.app_name}:{self.value}"

    def get_tuple(self):
        return f"{self.app_name}:{self.value}", self.description

    def get_dict(self):
        _dict = {}
        dict_index = f"{self.app_name}:{self.value}"
        _dict[dict_index] = self.description
        return _dict
