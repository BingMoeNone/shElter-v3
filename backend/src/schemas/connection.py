from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from src.schemas.user import UserResponse


class ConnectionCreate(BaseModel):
    user_id: str
    connection_type: str


class ConnectionResponse(BaseModel):
    id: str
    follower: UserResponse
    followed: UserResponse
    status: str
    connection_type: str
    created_at: datetime
    accepted_at: Optional[datetime]

    class Config:
        from_attributes = True
