import uuid
from datetime import datetime
from typing import Optional, List

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship

from src.database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False)
    slug = Column(String(250), unique=True, nullable=False, index=True)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    status = Column(String(20), default="draft", nullable=False)
    author_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    view_count = Column(Integer, default=0, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)
    is_approved = Column(Boolean, default=True, nullable=False)

    author = relationship("User", back_populates="articles")
    revisions = relationship("Revision", back_populates="article", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="article", cascade="all, delete-orphan")
    categories = relationship(
        "Category", secondary="article_categories", back_populates="articles"
    )
    tags = relationship(
        "Tag", secondary="article_tags", back_populates="articles"
    )
