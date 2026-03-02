# -*- coding: utf-8 -*-
"""
项目配置文件
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """
    项目配置类
    """
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./wiki_platform.db"  # 数据库连接URL
    
    # JWT配置 - HS256 (HMAC算法)
    SECRET_KEY: str = "f82b7d3e-4a1c-4e8f-9a2b-3c4d-5e6f-7a8b-9c0d"  # 密钥
    ALGORITHM: str = "HS256"  # 算法
    PRIVATE_KEY_PATH: str = ""  # 私钥路径
    PUBLIC_KEY_PATH: str = ""  # 公钥路径
    
    # Token过期时间
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 访问令牌过期时间（分钟）
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # 刷新令牌过期时间（天）
    
    # 安全配置
    CORS_ORIGINS: List[str] = ["http://localhost:8080", "http://127.0.0.1:8080", "http://127.0.0.1:5500"]  # 允许的CORS源
    DEBUG: bool = False  # 调试模式
    
    # 速率限制配置
    RATE_LIMIT_ENABLED: bool = True  # 是否启用速率限制
    RATE_LIMIT_LOGIN: str = "10/minute"  # 登录接口速率限制
    RATE_LIMIT_REGISTER: str = "5/minute"  # 注册接口速率限制
    RATE_LIMIT_DEFAULT: str = "60/minute"  # 默认速率限制

    # 模型配置
    model_config = {
        "env_file": ".env",  # 环境变量文件
        "case_sensitive": True,  # 大小写敏感
        "extra": "ignore"  # 允许环境变量中有额外的字段
    }


# 创建配置实例
settings = Settings()
