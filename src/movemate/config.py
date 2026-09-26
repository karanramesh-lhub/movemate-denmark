from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    app_name: str = "MoveMate Denmark"

    database_url: str = (
        "postgresql+asyncpg://movemate:movemate@localhost:5432/movemate"
    )

    qdrant_url: str = "http://localhost:6333"

    langfuse_base_url: str = "https://cloud.langfuse.com"
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_tracing_environment: str = "development"

    llm_provider: str = ""
    llm_api_key: str = ""
    llm_model: str = ""
    llm_timeout_ms: int = 120000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()