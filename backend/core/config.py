from typing import Optional, Dict, Any
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, validator
import secrets
from functools import lru_cache

class Settings(BaseSettings):
    # Project Info
    PROJECT_NAME: str = "TagFlow"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str = "5432"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",  # React default
        "http://localhost:3001",  # Alternative port
        "http://localhost:8080",  # Alternative port
    ]

    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # Redis (for caching)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: list[str] = ["txt", "pdf", "doc", "docx"]

    class Config:
        case_sensitive = True
        env_file = ".env"

# Create a cached instance of settings
@lru_cache()
def get_settings() -> Settings:
    return Settings()

# Export settings instance
settings = get_settings() 