from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str = Field(..., min_length=8)
    display_name: Optional[str] = Field(None, max_length=50)


class UserUpdate(BaseModel):
    display_name: Optional[str] = Field(None, max_length=50)
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    display_name: Optional[str]
    bio: Optional[str]
    avatar_url: Optional[str]
    level: int
    is_active: bool
    role: str
    created_at: datetime
    updated_at: datetime
    contribution_count: int

    class Config:
        from_attributes = True


class UserContributionStats(BaseModel):
    total_articles: int
    total_comments: int
    total_revisions: int
    total_connections: int
    contribution_count: int
    recent_articles: int = Field(..., description="Number of articles created in the last 30 days")
    recent_comments: int = Field(..., description="Number of comments created in the last 30 days")


class UserProfileResponse(BaseModel):
    id: str
    username: str
    display_name: Optional[str]
    bio: Optional[str]
    avatar_url: Optional[str]
    level: int
    created_at: datetime
    contribution_count: int
    is_following: bool = False
    stats: Optional[UserContributionStats] = None

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=8)


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse
