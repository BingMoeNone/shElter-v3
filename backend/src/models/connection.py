import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Connection(Base):
    __tablename__ = "connections"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    follower_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    followed_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    status = Column(String(20), default="pending", nullable=False)
    connection_type = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    accepted_at = Column(DateTime, nullable=True)

    follower = relationship("User", foreign_keys=[follower_id], back_populates="follower_connections")
    followed = relationship("User", foreign_keys=[followed_id], back_populates="followed_connections")
