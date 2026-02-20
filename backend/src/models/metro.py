from typing import List, Optional
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from src.database import Base

class Station(Base):
    """
    Represents a Metro Station (from v1 directory structure).
    """
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    path_key = Column(String, unique=True, nullable=False)  # e.g., "01_Cryptonomicon"
    min_level = Column(Integer, default=1, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    meta_data = Column(JSON, default={}, nullable=False)  # UI coordinates, icon config

    # Relationships
    lines = relationship("StationLineJunction", back_populates="station")


class Line(Base):
    """
    Represents a Metro Line connecting stations.
    """
    __tablename__ = "lines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # e.g., "Line 1"
    color = Column(String, nullable=False)  # e.g., "#FF0000"
    required_level = Column(Integer, default=1, nullable=False)

    # Relationships
    stations = relationship("StationLineJunction", back_populates="line")


class StationLineJunction(Base):
    """
    Many-to-Many relationship between Station and Line with ordering.
    """
    __tablename__ = "station_line_junction"

    station_id = Column(Integer, ForeignKey("stations.id"), primary_key=True)
    line_id = Column(Integer, ForeignKey("lines.id"), primary_key=True)
    order_index = Column(Integer, nullable=False)

    station = relationship("Station", back_populates="lines")
    line = relationship("Line", back_populates="stations")
