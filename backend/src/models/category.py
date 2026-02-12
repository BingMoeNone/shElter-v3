import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(120), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    parent_id = Column(String(36), ForeignKey("categories.id"), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    article_count = Column(Integer, default=0, nullable=False)

    parent = relationship("Category", remote_side=[id], backref="children")
    articles = relationship(
        "Article", secondary="article_categories", back_populates="categories"
    )
