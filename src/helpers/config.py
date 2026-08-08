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

    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    OPENAI_API_KEY: str = None
    OPENAI_API_URL: str = None
    COHERE_API_KEY: str = None

    GENERATION_MODEL_ID: str = None
    EMBEDDING_MODEL_ID: str = None
    EMBEDDING_MODEL_SIZE: int = None
    INPUT_DAFAULT_MAX_CHARACTERS: int = None
    GENERATION_DAFAULT_MAX_TOKENS: int = None
    GENERATION_DAFAULT_TEMPERATURE: float = None 

    VECTOR_DB_BACKEND : str
    VECTOR_DB_PATH : str
    VECTOR_DB_DISTANCE_METHOD: str = None

    DEFAULT_LANG : str
    PRIMARY_LANG : str
    SECONDARY_LANG : str

    # Note: In Pydantic v2, we use model_config rather than class Config
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# The decorator keeps the instance in memory after the first call
@lru_cache
def get_settings() -> Settings:
    return Settings()