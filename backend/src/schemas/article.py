from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field

from src.schemas.user import UserResponse
from src.schemas.category import CategoryResponse
from src.schemas.tag import TagResponse


class ArticleCreate(BaseModel):
    title: str = Field(..., max_length=200)
    content: str = Field(..., min_length=10)
    summary: Optional[str] = Field(None, max_length=500)
    status: str = "draft"
    category_ids: Optional[List[UUID]] = None
    tag_names: Optional[List[str]] = None


class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = Field(None, min_length=10)
    summary: Optional[str] = Field(None, max_length=500)
    status: Optional[str] = None
    category_ids: Optional[List[UUID]] = None
    tag_names: Optional[List[str]] = None


class ArticleResponse(BaseModel):
    id: UUID
    title: str
    slug: str
    content: str
    summary: Optional[str]
    status: str
    author: UserResponse
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    view_count: int
    is_featured: bool
    categories: List[CategoryResponse] = []
    tags: List[TagResponse] = []

    class Config:
        from_attributes = True


class ArticleListResponse(BaseModel):
    articles: List[ArticleResponse]
    pagination: dict


class RevisionResponse(BaseModel):
    id: UUID
    article_id: UUID
    author: UserResponse
    title: str
    content: str
    change_summary: Optional[str]
    revision_number: int
    created_at: datetime

    class Config:
        from_attributes = True
