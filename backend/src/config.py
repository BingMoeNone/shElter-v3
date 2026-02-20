from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./wiki_platform.db"
    
    # JWT Configuration - RS256 (升级版)
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "RS256"
    PRIVATE_KEY_PATH: str = "keys/private_key.pem"
    PUBLIC_KEY_PATH: str = "keys/public_key.pem"
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Security
    CORS_ORIGINS: List[str] = ["*"]
    DEBUG: bool = False
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_LOGIN: str = "10/minute"
    RATE_LIMIT_REGISTER: str = "5/minute"
    RATE_LIMIT_DEFAULT: str = "60/minute"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
