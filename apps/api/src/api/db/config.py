from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve the absolute path to the root directory (one level up from this file's folder)
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ROOT_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str

    frontend_url: str = "http://localhost:3000"

    api_key: str = "super_secret_api_key" 

    db_timezone: str = "UTC"

settings = Settings()
