import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Text, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    content = Column(Text, nullable=False)
    author_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    article_id = Column(String(36), ForeignKey("articles.id"), nullable=False, index=True)
    parent_id = Column(String(36), ForeignKey("comments.id"), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_approved = Column(Boolean, default=True, nullable=False)

    author = relationship("User", back_populates="comments")
    article = relationship("Article", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], backref="replies")
