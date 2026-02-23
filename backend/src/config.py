from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./wiki_platform.db"
    
    # JWT Configuration - RS256 (RSA algorithm)
    SECRET_KEY: str = "f82b7d3e-4a1c-4e8f-9a2b-3c4d-5e6f-7a8b-9c0d"
    ALGORITHM: str = "RS256"
    PRIVATE_KEY_PATH: str = "keys/private_key.pem"
    PUBLIC_KEY_PATH: str = "keys/public_key.pem"
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Security
    CORS_ORIGINS: List[str] = ["http://localhost:8080", "http://127.0.0.1:8080"]
    DEBUG: bool = False
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_LOGIN: str = "10/minute"
    RATE_LIMIT_REGISTER: str = "5/minute"
    RATE_LIMIT_DEFAULT: str = "60/minute"

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore"  # 允许环境变量中有额外的字段
    }


settings = Settings()
