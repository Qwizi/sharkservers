from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    TESTING: bool = False
    SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES: int = 5
    REFRESH_TOKEN_EXPIRES: int = 43829
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    STEAM_API_KEY: str
    DEBUG: bool = False
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    IMAGE_ALLOWED_EXTENSIONS: list = [".png", ".jpg", ".jpeg"]
    IMAGE_ALLOWED_CONTENT_TYPES: list = ["image/png", "image/jpeg"]
    AVATAR_MAX_SIZE: int = 1024 * 1024 * 2 # 2MB
    AVATAR_HEIGHT: int = 100
    AVATAR_WIDTH: int = 100
    STRIPE_API_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    SITE_URL: str = "http://localhost:80"

    class Config:
        env_file = ".env"

    def get_database_url(self):
        if self.TESTING:
            return "sqlite:///../test.db"
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}"

    def get_database_url_sync(self):
        if self.TESTING:
            return "sqlite:///test.db"
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}"

    def get_redis_url(self):
        if self.TESTING:
            return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/1"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"


@lru_cache()
def get_settings():
    return Settings()
