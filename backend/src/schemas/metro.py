from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class StationBase(BaseModel):
    name: str
    path_key: str
    description: Optional[str] = None
    min_level: int = 1
    meta_data: Dict[str, Any] = {}

class Station(StationBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True

class LineBase(BaseModel):
    name: str
    color: str
    required_level: int = 1

class Line(LineBase):
    id: int
    
    class Config:
        from_attributes = True

class StationWithLines(Station):
    lines: List[Line] = []
