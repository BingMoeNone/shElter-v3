from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+")
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        description="Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character"
    )
    display_name: Optional[str] = Field(None, max_length=50)


class UserUpdate(BaseModel):
    display_name: Optional[str] = Field(None, max_length=50)
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    display_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True


class UserProfileResponse(UserResponse):
    followers_count: int = 0
    following_count: int = 0
    articles_count: int = 0
    comments_count: int = 0


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class UserContributionStats(BaseModel):
    total_articles: int
    total_comments: int
    total_revisions: int
    articles_by_category: dict[str, int]
    recent_activity: List[dict]


class AdminUserResponse(UserResponse):
    last_login_at: Optional[datetime] = None


class AdminUserUpdate(BaseModel):
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    display_name: Optional[str] = Field(None, max_length=50)
    bio: Optional[str] = Field(None, max_length=500)


class AdminPasswordReset(BaseModel):
    user_id: int
    new_password: str = Field(
        ...,
        min_length=8,
        description="Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character"
    )