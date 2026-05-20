from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str = Field(alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4.1-mini", alias="OPENAI_MODEL")
    embedding_model: str = Field(default="text-embedding-3-small", alias="EMBEDDING_MODEL")
    persist_directory: str = Field(default="./chroma_langchain.db", alias="PERSIST_DIRECTORY")
    pdf_collection_name: str = Field(default="pdf_market_reports", alias="PDF_COLLECTION_NAME")
    csv_collection_name: str = Field(default="google_play_apps", alias="CSV_COLLECTION_NAME")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()