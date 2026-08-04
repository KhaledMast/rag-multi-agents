from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str

    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    MONGODB_URL: str
    MONGODB_DATABASE: str   

    # Note: In Pydantic v2, we use model_config rather than class Config
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# The decorator keeps the instance in memory after the first call
@lru_cache
def get_settings() -> Settings:
    return Settings()