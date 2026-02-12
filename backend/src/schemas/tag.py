from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class TagResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    usage_count: int

    class Config:
        from_attributes = True


class TagCreate(BaseModel):
    name: str


class TagUpdate(BaseModel):
    name: str
