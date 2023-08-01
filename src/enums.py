from enum import Enum


class MainEventEnum(str, Enum):
    STARTUP = "MAIN_STARTUP"
    SHUTDOWN = "MAIN_SHUTDOWN"
    INSTALL = "MAIN_INSTALL"


class ActivationEmailTypeEnum(str, Enum):
    ACCOUNT = "account"
    EMAIL = "email"
    PASSWORD = "password"
