import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(30), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(50), nullable=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(String(20), default="user", nullable=False)
    contribution_count = Column(Integer, default=0, nullable=False)

    articles = relationship("Article", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    revisions = relationship("Revision", back_populates="author")
    follower_connections = relationship(
        "Connection", foreign_keys="Connection.follower_id", back_populates="follower"
    )
    followed_connections = relationship(
        "Connection", foreign_keys="Connection.followed_id", back_populates="followed"
    )
