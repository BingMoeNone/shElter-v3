from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./wiki_platform.db"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    CORS_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
