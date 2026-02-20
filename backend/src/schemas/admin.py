from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field


class AdminUserResponse(BaseModel):
    id: str
    username: str
    email: str
    display_name: Optional[str]
    bio: Optional[str]
    avatar_url: Optional[str]
    is_active: bool
    role: str
    created_at: datetime
    updated_at: datetime
    contribution_count: int

    class Config:
        from_attributes = True


class AdminUserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    email: Optional[EmailStr] = None
    display_name: Optional[str] = Field(None, max_length=50)
    bio: Optional[str] = Field(None, max_length=500)
    role: Optional[str] = Field(None, pattern=r"^(user|moderator|admin)$")
    is_active: Optional[bool] = None


class AdminPasswordReset(BaseModel):
    new_password: str = Field(..., min_length=8)


class AuditLogResponse(BaseModel):
    id: str
    operator_id: str
    operator_username: str
    action: str
    target_type: str
    target_id: Optional[str]
    target_info: Optional[str]
    details: Optional[str]
    ip_address: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
