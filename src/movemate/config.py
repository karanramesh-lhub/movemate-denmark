from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "development"
    app_name: str = "MoveMate Denmark"

    database_url: str = (
        "postgresql+asyncpg://movemate:movemate@localhost:5432/movemate"
    )

    qdrant_url: str = "http://localhost:6333"

    langfuse_host: str = "http://localhost:3000"
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""

    llm_provider: str = ""
    llm_api_key: str = ""
    llm_model: str = ""

    class Config:
        env_file = ".env"


settings = Settings()