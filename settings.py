from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # TODO: Remove unneeded configs from env
    # Main branch configs
    DJANGO_SECRET_KEY: str
    DJANGO_DEBUG: str
    DJANGO_ALLOWED_HOSTS: str
    DJANGO_DATABASE_ENGINE: str

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_INITDB_DATABASE: str
    MONGODB_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRES_DELTA_IN_MINUTES: int


default_settings = Settings()
