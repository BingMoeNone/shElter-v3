# -*- coding: utf-8 -*-
"""
后端主入口文件
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
import os
import time

from src.api import (
    auth_router,          # 认证相关API
    users_router,         # 用户相关API
    articles_router,      # 文章相关API
    categories_router,    # 分类相关API
    tags_router,          # 标签相关API
    comments_router,      # 评论相关API
    connections_router,   # 连接相关API
    search_router,        # 搜索相关API
    admin_router,         # 管理员相关API
    metro_router,         # 地铁相关API
    music_router,         # 音乐相关API
    media_router,         # 媒体相关API
    moderation_router,    # 内容审核相关API
)
from src.config import settings
from src.core.response import response_wrapper
from src.core.security import limiter


# 创建FastAPI应用实例
app = FastAPI(
    title="Wiki Platform API",
    description="API for the wiki platform with article management, user profiles, and social features",
    version="1.1.0",
    docs_url="/api/docs",     # API文档地址
    redoc_url="/api/redoc",   # ReDoc文档地址
    openapi_url="/api/openapi.json",  # OpenAPI规范地址
    redirect_slashes=False,    # 禁用末尾斜杠重定向
)

# 设置速率限制器
app.state.limiter = limiter


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    HTTP异常处理器
    
    Args:
        request: 请求对象
        exc: HTTP异常对象
    
    Returns:
        JSONResponse: 格式化的错误响应
    """
    if isinstance(exc.detail, dict):
        detail = exc.detail
        message = detail.get("message", str(exc.detail))
        error_code = detail.get("error_code", "ERROR")
    else:
        message = str(exc.detail)
        error_code = "ERROR"

    return JSONResponse(
        status_code=exc.status_code,
        content=response_wrapper.error(
            message=message,
            error_code=error_code,
            status_code=exc.status_code,
        ),
    )


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """
    速率限制异常处理器
    
    Args:
        request: 请求对象
        exc: 速率限制异常对象
    
    Returns:
        JSONResponse: 格式化的错误响应
    """
    return JSONResponse(
        status_code=429,
        content=response_wrapper.error(
            message="请求过于频繁，请稍后再试",
            error_code="RATE_LIMIT_EXCEEDED",
            status_code=429,
        ),
    )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    添加处理时间中间件
    
    Args:
        request: 请求对象
        call_next: 下一个中间件或路由处理函数
    
    Returns:
        Response: 响应对象
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)  # 添加处理时间
    return response


# 添加CORS中间件 - 从配置文件读取
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # 从配置文件读取允许的源
    allow_credentials=True,  # 允许携带凭证
    allow_methods=["*"],  # 允许的HTTP方法
    allow_headers=["*"],  # 允许的HTTP头
)


# 注册API路由
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])  # 认证路由
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])  # 用户路由
app.include_router(articles_router, prefix="/api/v1/articles", tags=["articles"])  # 文章路由
app.include_router(categories_router, prefix="/api/v1/categories", tags=["categories"])  # 分类路由
app.include_router(tags_router, prefix="/api/v1/tags", tags=["tags"])  # 标签路由
app.include_router(comments_router, prefix="/api/v1/comments", tags=["comments"])  # 评论路由
app.include_router(
    connections_router, prefix="/api/v1/connections", tags=["connections"]
)  # 连接路由
app.include_router(search_router, prefix="/api/v1/search", tags=["search"])  # 搜索路由
app.include_router(admin_router, prefix="/api/v1/admin", tags=["admin"])  # 管理员路由
app.include_router(metro_router, prefix="/api/v1/metro", tags=["metro"])  # 地铁路由
app.include_router(music_router, prefix="/api/v1/music", tags=["music"])  # 音乐路由
app.include_router(media_router, prefix="/api/v1/media", tags=["media"])  # 媒体路由
app.include_router(moderation_router, prefix="/api/v1/moderation", tags=["moderation"])  # 内容审核路由


# 挂载静态文件
try:
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")

        # 挂载音乐文件目录
        music_dir = os.path.join(static_dir, "music")
        if os.path.exists(music_dir):
            app.mount("/music", StaticFiles(directory=music_dir), name="music")
except Exception as e:
    print(f"挂载静态文件时出错: {e}")


@app.get("/health")
async def health_check():
    """
    健康检查端点
    
    Returns:
        dict: 健康状态信息
    """
    return {"status": "healthy", "version": "1.1.0"}


@app.get("/")
async def root():
    """
    根路由
    
    Returns:
        dict: API基本信息
    """
    return response_wrapper.success(
        data={"name": "Wiki Platform API", "version": "1.1.0", "docs": "/api/docs"},
        message="欢迎使用 Wiki Platform API",
    )
