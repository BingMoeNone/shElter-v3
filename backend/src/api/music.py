from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database.connection import get_db
from src.models.music import Track, Album, Artist
from src.schemas.music import Track as TrackSchema, Album as AlbumSchema, Artist as ArtistSchema

router = APIRouter()

@router.get("/tracks", response_model=List[TrackSchema])
def get_tracks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    tracks = db.query(Track).offset(skip).limit(limit).all()
    return tracks

@router.get("/albums", response_model=List[AlbumSchema])
def get_albums(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    albums = db.query(Album).offset(skip).limit(limit).all()
    return albums

@router.get("/artists", response_model=List[ArtistSchema])
def get_artists(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    artists = db.query(Artist).offset(skip).limit(limit).all()
    return artists
