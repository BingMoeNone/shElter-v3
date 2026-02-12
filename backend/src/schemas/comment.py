from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

from src.schemas.user import UserResponse


class CommentCreate(BaseModel):
    article_id: UUID
    content: str = Field(..., min_length=1, max_length=10000)
    parent_id: Optional[UUID] = None


class CommentUpdate(BaseModel):
    content: str = Field(..., min_length=1, max_length=10000)


class CommentResponse(BaseModel):
    id: UUID
    content: str
    author: UserResponse
    article_id: UUID
    parent_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime
    is_approved: bool

    class Config:
        from_attributes = True
