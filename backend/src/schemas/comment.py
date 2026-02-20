from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from src.schemas.user import UserResponse


class CommentCreate(BaseModel):
    article_id: str
    content: str = Field(..., min_length=1, max_length=10000)
    parent_id: Optional[str] = None


class CommentUpdate(BaseModel):
    content: str = Field(..., min_length=1, max_length=10000)


class CommentResponse(BaseModel):
    id: str
    content: str
    author: UserResponse
    article_id: str
    parent_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    is_approved: bool

    class Config:
        from_attributes = True
