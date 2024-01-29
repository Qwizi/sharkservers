"""Settings module."""
from __future__ import annotations

from functools import lru_cache

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """
    The Settings class represents the application's configuration settings.

    Attributes
    ----------
    POSTGRES_HOST (str): The hostname of the PostgreSQL database server.
    POSTGRES_DB (str): The name of the PostgreSQL database.
    POSTGRES_USER (str): The username for connecting to the PostgreSQL database.
    POSTGRES_PASSWORD (str): The password for connecting to the PostgreSQL database.
    TESTING (bool): Flag indicating whether the application is running in testing mode. Default is False.
    SECRET_KEY (str): The secret key used for cryptographic operations.
    REFRESH_SECRET_KEY (str): The secret key used for refreshing access tokens.
    ALGORITHM (str): The algorithm used for token generation. Default is "HS256".
    ACCESS_TOKEN_EXPIRES (int): The expiration time (in minutes) for access tokens. Default is 5 minutes.
    REFRESH_TOKEN_EXPIRES (int): The expiration time (in minutes) for refresh tokens. Default is 43829 minutes.
    REDIS_HOST (str): The hostname of the Redis server. Default is "redis".
    REDIS_PORT (int): The port number of the Redis server. Default is 6379.
    STEAM_API_KEY (str): The API key for accessing the Steam API.
    DEBUG (bool): Flag indicating whether the application is running in debug mode. Default is False.
    MAIL_USERNAME (str): The username for the email server.
    MAIL_PASSWORD (str): The password for the email server.
    MAIL_FROM (str): The email address used as the "From" field in outgoing emails.
    MAIL_PORT (int): The port number of the email server.
    MAIL_SERVER (str): The hostname of the email server.
    MAIL_FROM_NAME (str): The name used as the "From" field in outgoing emails.
    MAIL_STARTTLS (bool): Flag indicating whether to use STARTTLS for secure email communication. Default is True.
    MAIL_SSL_TLS (bool): Flag indicating whether to use SSL/TLS for secure email communication. Default is False.
    USE_CREDENTIALS (bool): Flag indicating whether to use credentials for email communication. Default is True.
    VALIDATE_CERTS (bool): Flag indicating whether to validate SSL certificates for email communication. Default is True.
    IMAGE_ALLOWED_EXTENSIONS (list): List of allowed image file extensions. Default is [".png", ".jpg", ".jpeg"].
    AVATAR_WIDTH (int): The width of user avatars. Default is 100.
    STRIPE_API_KEY (str): The API key for accessing the Stripe API.
    STRIPE_WEBHOOK_SECRET (str): The secret key for verifying Stripe webhook events.
    SITE_URL (str): The base URL of the site. Default is "http://localhost:8080".

    Methods
    -------
    get_database_url(): Returns the database URL based on the configuration settings.
    get_database_url_sync(): Returns the synchronous database URL based on the configuration settings.
    get_redis_url(): Returns the Redis URL based on the configuration settings.
    """

    POSTGRES_HOST: str = ""
    POSTGRES_DB: str = ""
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    TESTING: bool = False
    SECRET_KEY: str = ""
    REFRESH_SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES: int = 5
    REFRESH_TOKEN_EXPIRES: int = 43829
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    STEAM_API_KEY: str = ""
    DEBUG: bool = False
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: EmailStr = ""
    MAIL_PORT: int = 587
    MAIL_SERVER: str = ""
    MAIL_FROM_NAME: str = ""
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    IMAGE_ALLOWED_EXTENSIONS: list[str] = [".png", ".jpg", ".jpeg"]
    AVATAR_WIDTH: int = 100
    STRIPE_API_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    SITE_URL: str = "http://localhost:8080"
    RESEND_API_KEY: str = ""

    class Config:
        """The Config class represents the configuration settings for the Settings class."""

        env_file = ".env"

    def get_database_url(self) -> str:
        """
        Return the database URL based on the configuration settings.

        Returns
        -------
        str: The database URL.
        """
        if self.TESTING:
            return "sqlite:///../test.db"
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}"

    def get_database_url_sync(self) -> str:
        """
        Return the synchronous database URL based on the configuration settings.

        Returns
        -------
        str: The synchronous database URL.
        """
        if self.TESTING:
            return "sqlite:///test.db"
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}"

    def get_redis_url(self) -> str:
        """
        Return the Redis URL based on the configuration settings.

        Returns
        -------
        str: The Redis URL.
        """
        if self.TESTING:
            return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/1"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"


@lru_cache
def get_settings() -> Settings:
    """
    Return an instance of the Settings class.

    Returns
    -------
    Settings: An instance of the Settings class.
    """
    return Settings()
