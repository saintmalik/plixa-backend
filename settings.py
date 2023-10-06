from typing import Literal, Annotated

from pydantic import Field, UrlConstraints
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

MongoSRVDsn = Annotated[MultiHostUrl, UrlConstraints(allowed_schemes=["mongodb+srv"])]


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
    EXPIRES_DELTA: int  # in minutes


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    MONGODB_DSN: MongoSRVDsn = Field(validation_alias="MONGODB_URL")
    JWT_SETTINGS: JWTSettings = JWTSettings()
    SMTP_SETTINGS: SMTPSettings = SMTPSettings()


default_settings = Settings()
