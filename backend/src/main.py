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
    articles,
    auth,
    categories,
    comments,
    connections,
    search,
    tags,
    users,
    admin,
    metro,
    music,
    media,
    moderation,
)
from src.config import settings
from src.core.response import response_wrapper
from src.core.security import limiter


app = FastAPI(
    title="Wiki Platform API",
    description="API for the wiki platform with article management, user profiles, and social features",
    version="1.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.state.limiter = limiter


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
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
    return JSONResponse(
        status_code=429,
        content=response_wrapper.error(
            message="璇锋眰杩囦簬棰戠箒锛岃绋嶅悗鍐嶈瘯",
            error_code="RATE_LIMIT_EXCEEDED",
            status_code=429,
        ),
    )


app.add_middleware(SlowAPIMiddleware)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    if settings.DEBUG:
        response.headers["X-Debug-Mode"] = "enabled"

    return response


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(articles.router, prefix="/api/v1/articles", tags=["articles"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(tags.router, prefix="/api/v1/tags", tags=["tags"])
app.include_router(comments.router, prefix="/api/v1/comments", tags=["comments"])
app.include_router(
    connections.router, prefix="/api/v1/connections", tags=["connections"]
)
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])
app.include_router(metro.router, prefix="/api/v1/metro", tags=["metro"])
app.include_router(music.router, prefix="/api/v1/music", tags=["music"])
app.include_router(media.router, prefix="/api/v1/media", tags=["media"])
app.include_router(moderation.router, prefix="/api/v1/moderation", tags=["moderation"])


static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    music_dir = os.path.join(static_dir, "music")
    if os.path.exists(music_dir):
        app.mount("/music", StaticFiles(directory=music_dir), name="music")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.1.0"}


@app.get("/")
async def root():
    return response_wrapper.success(
        data={"name": "Wiki Platform API", "version": "1.1.0", "docs": "/api/docs"},
        message="娆㈣繋浣跨敤 Wiki Platform API",
    )
