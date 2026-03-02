# -*- coding: utf-8 -*-
"""
文章模型
"""
import uuid
from datetime import datetime
from typing import Optional, List

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship

from src.database import Base


class Article(Base):
    """
    文章模型类
    """
    __tablename__ = "articles"  # 表名

    # 主键和基本信息
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # 文章ID，使用UUID
    title = Column(String(200), nullable=False)  # 标题
    slug = Column(String(250), unique=True, nullable=False, index=True)  #  slug，用于URL
    content = Column(Text, nullable=False)  # 内容
    summary = Column(Text, nullable=True)  # 摘要
    status = Column(String(20), default="draft", nullable=False)  # 状态（draft/published）
    
    # 作者信息
    author_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)  # 作者ID
    
    # 时间戳
    published_at = Column(DateTime, nullable=True)  # 发布时间
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)  # 创建时间
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)  # 更新时间
    
    # 统计和状态
    view_count = Column(Integer, default=0, nullable=False)  # 浏览次数
    is_featured = Column(Boolean, default=False, nullable=False)  # 是否精选
    is_approved = Column(Boolean, default=True, nullable=False)  # 是否审核通过

    # 关系
    author = relationship("User", back_populates="articles")  # 作者关系
    revisions = relationship("Revision", back_populates="article", cascade="all, delete-orphan")  # 修订关系
    comments = relationship("Comment", back_populates="article", cascade="all, delete-orphan")  # 评论关系
    categories = relationship(
        "Category", secondary="article_categories", back_populates="articles"
    )  # 分类关系
    tags = relationship(
        "Tag", secondary="article_tags", back_populates="articles"
    )  # 标签关系
