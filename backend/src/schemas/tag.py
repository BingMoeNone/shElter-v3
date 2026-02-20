from datetime import datetime
from pydantic import BaseModel


class TagResponse(BaseModel):
    id: str
    name: str
    slug: str
    usage_count: int

    class Config:
        from_attributes = True


class TagCreate(BaseModel):
    name: str


class TagUpdate(BaseModel):
    name: str
