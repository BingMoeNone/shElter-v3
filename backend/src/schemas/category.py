from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class CategoryResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: Optional[str]
    parent_id: Optional[UUID]
    article_count: int

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[UUID] = None


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[UUID] = None
