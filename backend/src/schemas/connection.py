from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from src.schemas.user import UserResponse


class ConnectionCreate(BaseModel):
    user_id: UUID
    connection_type: str


class ConnectionResponse(BaseModel):
    id: UUID
    follower: UserResponse
    followed: UserResponse
    status: str
    connection_type: str
    created_at: datetime
    accepted_at: Optional[datetime]

    class Config:
        from_attributes = True
