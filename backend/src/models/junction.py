import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, ForeignKey, Table
from src.database import Base


article_categories = Table(
    "article_categories",
    Base.metadata,
    Column("article_id", String(36), ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", String(36), ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
    Column("assigned_at", DateTime, default=datetime.utcnow, nullable=False),
)

article_tags = Table(
    "article_tags",
    Base.metadata,
    Column("article_id", String(36), ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", String(36), ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
    Column("assigned_at", DateTime, default=datetime.utcnow, nullable=False),
)
