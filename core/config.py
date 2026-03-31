# config.py
from pydantic_settings import BaseSettings  # pip install pydantic-settings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    # App
    app_name: str = "Learning Backend"
    environment: str = "development"  # development | staging | production
    debug: bool = False

    # Auth
    jwt_secret_key: str  # required — no default

    # Database
    database_url: Optional[str] = None  # required — no default
    sync_database_url: Optional[str] = None  # for Alembic — auto-generated if not set

    # Redis
    # redis_url: str = "redis://localhost:6379"

    model_config = {"env_file": ".env"}  # reads from .env automatically


@lru_cache
def get_settings() -> Settings:
    return Settings()
