from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Qdrant
    QDRANT_URL: str = "http://localhost:6333"
    COLLECTION_NAME: str = "production_rag"
    VECTOR_SIZE: int = 384

    # LLM - Gemini
    GEMINI_API_KEY: str

    # App
    PROJECT_NAME: str = "soumyo-production-rag-service"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
