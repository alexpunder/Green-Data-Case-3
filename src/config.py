from pydantic import ConfigDict, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class CustomBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class PostgresConfig(CustomBaseSettings):
    PROTOCOL: str = "postgresql+asyncpg"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "1234qaz"
    DB_NAME: str = "postgres"
    POOL_SIZE: int = 16
    POOL_TTL: int = 60 * 20
    POOL_PRE_PING: bool = True
    ECHO: bool = True

    model_config = ConfigDict(env_prefix="POSTGRES_")

    @property
    def postgres_dsn(self) -> PostgresDsn:
        return (
            f"{self.PROTOCOL}://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


class OllamaModelConfig(CustomBaseSettings):
    MODEL_NAME: str = "qwen2.5-coder:7b"
    MODEL_HOST: str = "localhost"
    MODEL_PORT: str = "11434"

    @property
    def model_dsn(self) -> str:
        return f"http://{self.MODEL_HOST}:{self.MODEL_PORT}"


class Config(CustomBaseSettings):
    pg_conf: PostgresConfig = PostgresConfig()
    ollama_conf: OllamaModelConfig = OllamaModelConfig()


conf = Config()
