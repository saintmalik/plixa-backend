from typing import Literal

from pydantic import MongoDsn, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SMTPSettings(BaseSettings):
    """Configurations for sending emails via SMTP."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="SMTP_", extra="ignore"
    )

    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    SECURITY: Literal["tls", "ssl"] | None = None


class JWTSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="JWT_", extra="ignore"
    )
    SECRET_KEY: str
    ALGORITHM: str
    EXPIRES_DELTA: str  # in minutes


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    MONGODB_DSN: MongoDsn = Field(validation_alias="MONGODB_URL")
    JWT_SETTINGS: JWTSettings = JWTSettings()
    SMTP_SETTINGS: SMTPSettings = SMTPSettings()


default_settings = Settings()
