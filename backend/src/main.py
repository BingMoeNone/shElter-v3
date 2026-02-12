from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import articles, auth, categories, comments, connections, search, tags, users
from src.config import settings

app = FastAPI(
    title="Wiki Platform API",
    description="API for the wiki platform with article management, user profiles, and social features",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

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
app.include_router(connections.router, prefix="/api/v1/connections", tags=["connections"])
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
