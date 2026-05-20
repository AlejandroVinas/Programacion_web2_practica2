from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración centralizada del backend Python."""

    port: int = Field(default=3000, alias="PORT")
    jwt_secret: str = Field(default="dev-secret-change-me-minimum-32-bytes", alias="JWT_SECRET")
    jwt_expires_minutes: int = Field(default=60, alias="JWT_EXPIRES_MINUTES")
    database_url: str = Field(default="data/app.db", alias="DATABASE_URL")
    upload_dir: str = Field(default="uploads", alias="UPLOAD_DIR")
    frontend_origin: str = Field(default="http://localhost:5173", alias="FRONTEND_ORIGIN")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def database_path(self) -> Path:
        return Path(self.database_url)

    @property
    def upload_path(self) -> Path:
        return Path(self.upload_dir)


@lru_cache
def get_settings() -> Settings:
    return Settings()
