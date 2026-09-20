from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    SECRET_KEY: str = "chave-secreta-de-desenvolvimento-troque-em-producao"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "sqlite:///./agendamento.db"
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "https://recepcao.clinica-parceira.com"
    ]


settings = Settings()
