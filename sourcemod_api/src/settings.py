from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    TESTING: bool = False

    class Config:
        env_file = ".env"

    def get_database_url(self):
        if self.TESTING:
            return "sqlite:///../test.db"
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}"
    

@lru_cache()
def get_settings():
    return Settings()