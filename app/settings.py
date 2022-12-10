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

    class Config:
        env_file = '.env'

    def get_database_url(self):
        if self.TESTING:
            return "sqlite:///test.db"
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}"

    def get_redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"


@lru_cache()
def get_settings():
    return Settings()
