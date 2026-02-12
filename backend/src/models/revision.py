import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Revision(Base):
    __tablename__ = "revisions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    article_id = Column(String(36), ForeignKey("articles.id"), nullable=False, index=True)
    author_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    change_summary = Column(Text, nullable=True)
    revision_number = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    article = relationship("Article", back_populates="revisions")
    author = relationship("User", back_populates="revisions")
