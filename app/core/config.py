from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "mini user project management api"
    app_version: str = "1.0.0"
    database_url: str = Field(
        default="postgresql+asyncpg://user:password@db/appdb",
        validation_alias="DATABASE_URL",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
