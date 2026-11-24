from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str

    FILE_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    MONGODB_URL: str
    MONGODB_DATABASE: str  

    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str
    RERANK_BACKEND: str

    OPENAI_API_KEY: Optional[SecretStr] = None
    OPENAI_API_URL: Optional[str] = None
    COHERE_API_KEY: Optional[SecretStr] = None

    GENERATION_MODEL_ID: Optional[str] = None
    EMBEDDING_MODEL_ID: Optional[str] = None
    EMBEDDING_MODEL_SIZE: Optional[int] = None
    RERANK_MODEL_ID: Optional[str] = None
    RERANK_TOP: int = 5

    INPUT_DEFAULT_MAX_CHARACTERS: Optional[int] = None
    GENERATION_DEFAULT_MAX_TOKENS: Optional[int] = None
    GENERATION_DEFAULT_TEMPERATURE: Optional[float] = None

    VECTOR_DB_BACKEND : str
    VECTOR_DB_PATH : str
    VECTOR_DB_DISTANCE_METHOD: Optional[str] = None

    DEFAULT_LANG : str
    PRIMARY_LANG : str
    SECONDARY_LANG : str

    # Note: In Pydantic v2, we use model_config rather than class Config
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# The decorator keeps the instance in memory after the first call
@lru_cache
def get_settings() -> Settings:
    return Settings()