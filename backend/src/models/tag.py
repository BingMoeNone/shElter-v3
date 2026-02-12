import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), unique=True, nullable=False)
    slug = Column(String(60), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    usage_count = Column(Integer, default=0, nullable=False)

    articles = relationship(
        "Article", secondary="article_tags", back_populates="tags"
    )
