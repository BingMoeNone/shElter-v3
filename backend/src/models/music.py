from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from src.database import Base

# Association tables
album_artists = Table(
    "album_artists",
    Base.metadata,
    Column("album_id", Integer, ForeignKey("albums.id"), primary_key=True),
    Column("artist_id", Integer, ForeignKey("artists.id"), primary_key=True),
)

track_artists = Table(
    "track_artists",
    Base.metadata,
    Column("track_id", Integer, ForeignKey("tracks.id"), primary_key=True),
    Column("artist_id", Integer, ForeignKey("artists.id"), primary_key=True),
)

class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String, nullable=True)
    
    # Relationships
    albums = relationship("Album", secondary=album_artists, back_populates="artists")
    tracks = relationship("Track", secondary=track_artists, back_populates="artists")

class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    cover_url = Column(String, nullable=True)
    release_date = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    
    # Relationships
    artists = relationship("Artist", secondary=album_artists, back_populates="albums")
    tracks = relationship("Track", back_populates="album", cascade="all, delete-orphan")

class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    duration = Column(Integer, nullable=True)  # in seconds
    file_url = Column(String, nullable=False)
    order = Column(Integer, default=0)  # Track number in album
    
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=True)
    
    # Relationships
    album = relationship("Album", back_populates="tracks")
    artists = relationship("Artist", secondary=track_artists, back_populates="tracks")
