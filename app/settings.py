import logging
from enum import Enum

from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

# https://docs.pydantic.dev/latest/concepts/pydantic_settings/


class CloudLogging(BaseModel):
    host: str
    token: str


class Environment(str, Enum):
    PRODUCTION = "production"
    DEVELOPMENT = "development"
    STAGING = "staging"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__", env_file=".env", env_file_encoding="utf-8"
    )

    debug: bool = Field(alias="DEBUG", default=False)
    database_url: PostgresDsn = Field(alias="DATABASE_URL")
    environment: Environment = Field(
        alias="ENVIRONMENT", default=Environment.DEVELOPMENT
    )
    allowed_hosts: list[str] = Field(alias="ALLOWED_HOSTS", default=["localhost"])
    cloud_logging: CloudLogging | None = Field(alias="CLOUD_LOGGING", default=None)


settings = Settings()  # type: ignore

logger = logging.getLogger(__name__)
logger.info(f"Current environment: {settings.environment}")
