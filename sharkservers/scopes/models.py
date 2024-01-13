"""Scopes models."""  # noqa: EXE002
import ormar

from sharkservers.db import BaseMeta


class Scope(ormar.Model):
    """
    Represents a scope in the application.

    Attributes
    ----------
        id (int): The unique identifier of the scope.
        app_name (str): The name of the application.
        value (str): The value of the scope.
        description (str): The description of the scope.
        protected (bool): Indicates if the scope is protected.

    Methods
    -------
        get_string(): Returns a string representation of the scope.
        get_tuple(): Returns a tuple representation of the scope.
        get_dict(): Returns a dictionary representation of the scope.
    """

    class Meta(BaseMeta):
        """Meta class for Scope model."""

        tablename = "scopes"

    id = ormar.Integer(primary_key=True)  # noqa: A003
    app_name = ormar.String(max_length=64)
    value = ormar.String(max_length=120)
    description = ormar.String(max_length=256)
    protected = ormar.Boolean(default=True)

    def get_string(self) -> str:
        """
        Return a string representation of the object.

        Returns
        -------
            str: The string representation of the object.
        """
        return f"{self.app_name}:{self.value}"

    def get_tuple(self) -> tuple:
        """
        Return a tuple containing the formatted app name and value, along with the description.

        Returns
        -------
            tuple: A tuple containing the formatted app name and value, along with the description.
        """  # noqa: E501
        return f"{self.app_name}:{self.value}", self.description

    def get_dict(self) -> dict:
        """
        Return a dictionary representation of the object.

        Returns
        -------
            dict: A dictionary with the object's attributes.
        """
        _dict = {}
        dict_index = f"{self.app_name}:{self.value}"
        _dict[dict_index] = self.description
        return _dict
