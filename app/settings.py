from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

# https://docs.pydantic.dev/latest/concepts/pydantic_settings/


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    debug: bool = Field(alias="DEBUG", default=False)
    database_url: PostgresDsn = Field(alias="DATABASE_URL")


settings = Settings()  # type: ignore
