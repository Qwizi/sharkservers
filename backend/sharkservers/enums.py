"""Module contains all the enums used in the project."""
from enum import Enum


class MainEventEnum(str, Enum):
    """
    Enum class representing main events.

    Attributes
    ----------
        STARTUP (str): Represents the startup event.
        SHUTDOWN (str): Represents the shutdown event.
        INSTALL (str): Represents the install event.
    """

    STARTUP = "MAIN_STARTUP"
    SHUTDOWN = "MAIN_SHUTDOWN"
    INSTALL = "MAIN_INSTALL"


class ActivationEmailTypeEnum(str, Enum):
    """
    Enum class representing activation email types.

    Attributes
    ----------
        ACCOUNT (str): Represents the account activation email type.
        EMAIL (str): Represents the email activation email type.
        PASSWORD (str): Represents the password activation email type.
    """

    ACCOUNT = "account"
    EMAIL = "email"
    PASSWORD = "password"  # noqa: S105


class OrderEnum(str, Enum):
    """
    Enum class representing order types.

    Attributes
    ----------
        ID_DESC (str): Represents the descending order by ID.
        ID_ASC (str): Represents the ascending order by ID.
    """

    ID_DESC = "-id"
    ID_ASC = "id"
