from typing import Generic, List, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class Pagination(BaseModel):
    page: int
    limit: int
    total_pages: int
    total_items: int


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    pagination: Pagination


class ErrorResponse(BaseModel):
    code: str
    message: str
    details: dict = {}
