from pydentic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    QDRANT_URL: str = "http://localhost:6333"
    COLLECTION_NAME: str = "production-rag"
    VECTOR_SIZE: int = 384
    PROJECT_NAME: str = "production-rag-service"
    
@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings=get_settings()