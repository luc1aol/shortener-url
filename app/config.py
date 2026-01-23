from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # PostgreSQL
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "urlshortener"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_TTL: int = 3600  # TTL en segundos para caché (1 hora)
    
    # Aplicación
    BASE_URL: str = "http://localhost:8000"
    CODE_LENGTH: int = 6  # Longitud del código de URL corta
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
