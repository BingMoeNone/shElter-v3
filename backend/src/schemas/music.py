from typing import List, Optional
from pydantic import BaseModel

class ArtistBase(BaseModel):
    name: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class Artist(ArtistBase):
    id: int
    
    class Config:
        from_attributes = True

class AlbumBase(BaseModel):
    title: str
    cover_url: Optional[str] = None
    release_date: Optional[str] = None
    description: Optional[str] = None

class Album(AlbumBase):
    id: int
    artists: List[Artist] = []
    
    class Config:
        from_attributes = True

class TrackBase(BaseModel):
    title: str
    file_url: str
    duration: Optional[int] = None
    order: int = 0
    album_id: Optional[int] = None

class Track(TrackBase):
    id: int
    album: Optional[Album] = None
    artists: List[Artist] = []
    
    class Config:
        from_attributes = True
