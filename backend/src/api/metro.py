from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database.connection import get_db
from src.models.metro import Station, Line
from src.schemas.metro import Station as StationSchema, Line as LineSchema

router = APIRouter()

@router.get("/stations", response_model=List[StationSchema])
def get_stations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    stations = db.query(Station).offset(skip).limit(limit).all()
    return stations

@router.get("/lines", response_model=List[LineSchema])
def get_lines(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    lines = db.query(Line).offset(skip).limit(limit).all()
    return lines

@router.get("/station/{path_key}", response_model=StationSchema)
def get_station_by_key(
    path_key: str,
    db: Session = Depends(get_db)
):
    station = db.query(Station).filter(Station.path_key == path_key).first()
    if not station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Station not found"
        )
    return station
