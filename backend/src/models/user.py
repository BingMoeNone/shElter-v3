# -*- coding: utf-8 -*-
"""
用户模型
"""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    """
    用户模型类
    """
    __tablename__ = "users"  # 表名

    # 主键和基本信息
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # 用户ID，使用UUID
    username = Column(String(30), nullable=False, index=True)  # 用户名
    email = Column(String(255), unique=True, nullable=False, index=True)  # 邮箱，唯一
    password_hash = Column(String(255), nullable=False)  # 密码哈希
    display_name = Column(String(50), nullable=True)  # 显示名称
    bio = Column(Text, nullable=True)  # 个人简介
    avatar_url = Column(String(500), nullable=True)  # 头像URL
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)  # 创建时间
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)  # 更新时间
    
    # 状态和权限
    is_active = Column(Boolean, default=True, nullable=False)  # 是否激活
    role = Column(String(20), default="user", nullable=False)  # 角色
    level = Column(Integer, default=1, nullable=False)  # 用户等级 (1-10)
    contribution_count = Column(Integer, default=0, nullable=False)  # 贡献次数

    # 关系
    articles = relationship("Article", back_populates="author")  # 文章关系
    comments = relationship("Comment", back_populates="author")  # 评论关系
    revisions = relationship("Revision", back_populates="author")  # 修订关系
    follower_connections = relationship(
        "Connection", foreign_keys="Connection.follower_id", back_populates="follower"
    )  # 关注者关系
    followed_connections = relationship(
        "Connection", foreign_keys="Connection.followed_id", back_populates="followed"
    )  # 被关注者关系
