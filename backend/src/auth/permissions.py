# -*- coding: utf-8 -*-
"""
权限管理模块

定义基于角色的访问控制(RBAC)相关功能
"""
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from src.database import get_db
from src.models import User
from src.auth.jwt import get_current_user


# 定义角色层级结构
ROLE_HIERARCHY = {
    "user": 1,
    "moderator": 2,
    "admin": 3
}

# 定义权限映射
PERMISSIONS = {
    "user": [
        "read_articles",
        "create_articles",
        "update_own_articles",
        "delete_own_articles",
        "read_users",
        "update_own_profile",
        "create_comments",
        "update_own_comments",
        "delete_own_comments",
        "manage_connections"
    ],
    "moderator": [
        "read_articles",
        "create_articles",
        "update_own_articles",
        "delete_own_articles",
        "update_any_articles",
        "delete_any_articles",
        "read_users",
        "update_own_profile",
        "create_comments",
        "update_own_comments",
        "delete_own_comments",
        "delete_any_comments",
        "manage_connections",
        "moderate_content",
        "view_audit_logs"
    ],
    "admin": [
        "read_articles",
        "create_articles",
        "update_own_articles",
        "delete_own_articles",
        "update_any_articles",
        "delete_any_articles",
        "read_users",
        "update_users",
        "delete_users",
        "update_own_profile",
        "create_comments",
        "update_own_comments",
        "delete_own_comments",
        "delete_any_comments",
        "manage_connections",
        "moderate_content",
        "view_audit_logs",
        "manage_roles",
        "system_config"
    ]
}


def has_role(current_user: User, required_role: str) -> bool:
    """
    检查用户是否具有指定角色或更高角色
    
    Args:
        current_user: 当前用户对象
        required_role: 需要的角色
    
    Returns:
        bool: 是否具有权限
    """
    user_role_level = ROLE_HIERARCHY.get(current_user.role, 0)
    required_role_level = ROLE_HIERARCHY.get(required_role, 0)
    return user_role_level >= required_role_level


def has_permission(current_user: User, permission: str) -> bool:
    """
    检查用户是否具有指定权限
    
    Args:
        current_user: 当前用户对象
        permission: 需要检查的权限
    
    Returns:
        bool: 是否具有权限
    """
    user_permissions = PERMISSIONS.get(current_user.role, [])
    return permission in user_permissions


def has_any_permission(current_user: User, permissions: List[str]) -> bool:
    """
    检查用户是否具有任意一个指定权限
    
    Args:
        current_user: 当前用户对象
        permissions: 需要检查的权限列表
    
    Returns:
        bool: 是否具有任意权限
    """
    user_permissions = PERMISSIONS.get(current_user.role, [])
    return any(perm in user_permissions for perm in permissions)


def has_all_permissions(current_user: User, permissions: List[str]) -> bool:
    """
    检查用户是否具有所有指定权限
    
    Args:
        current_user: 当前用户对象
        permissions: 需要检查的权限列表
    
    Returns:
        bool: 是否具有所有权限
    """
    user_permissions = PERMISSIONS.get(current_user.role, [])
    return all(perm in user_permissions for perm in permissions)


# 依赖项 - 角色检查
async def require_role(required_role: str):
    """
    角色检查依赖项
    
    Args:
        required_role: 需要检查的角色
    
    Returns:
        callable: 角色检查函数
    """
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if not has_role(current_user, required_role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "FORBIDDEN", "message": f"需要{required_role}权限"}
            )
        return current_user
    return role_checker


# 依赖项 - 权限检查
async def require_permission(permission: str):
    """
    权限检查依赖项
    
    Args:
        permission: 需要检查的权限
    
    Returns:
        callable: 权限检查函数
    """
    async def permission_checker(current_user: User = Depends(get_current_user)) -> User:
        if not has_permission(current_user, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "FORBIDDEN", "message": f"缺少{permission}权限"}
            )
        return current_user
    return permission_checker


# 依赖项 - 任意权限检查
async def require_any_permission(permissions: List[str]):
    """
    任意权限检查依赖项
    
    Args:
        permissions: 需要检查的权限列表
    
    Returns:
        callable: 权限检查函数
    """
    async def any_permission_checker(current_user: User = Depends(get_current_user)) -> User:
        if not has_any_permission(current_user, permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "FORBIDDEN", "message": f"缺少所需权限"}
            )
        return current_user
    return any_permission_checker


# 依赖项 - 所有权限检查
async def require_all_permissions(permissions: List[str]):
    """
    所有权限检查依赖项
    
    Args:
        permissions: 需要检查的权限列表
    
    Returns:
        callable: 权限检查函数
    """
    async def all_permission_checker(current_user: User = Depends(get_current_user)) -> User:
        if not has_all_permissions(current_user, permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "FORBIDDEN", "message": f"缺少所需权限"}
            )
        return current_user
    return all_permission_checker


# 文章权限检查
def can_edit_article(current_user: User, article_author_id: str) -> bool:
    """
    检查用户是否可以编辑文章
    
    Args:
        current_user: 当前用户对象
        article_author_id: 文章作者ID
    
    Returns:
        bool: 是否可以编辑
    """
    # 作者可以编辑自己的文章
    if str(current_user.id) == str(article_author_id):
        return True
    # 管理员和版主可以编辑所有文章
    return has_role(current_user, "moderator")


def can_delete_article(current_user: User, article_author_id: str) -> bool:
    """
    检查用户是否可以删除文章
    
    Args:
        current_user: 当前用户对象
        article_author_id: 文章作者ID
    
    Returns:
        bool: 是否可以删除
    """
    # 作者可以删除自己的文章
    if str(current_user.id) == str(article_author_id):
        return True
    # 管理员和版主可以删除所有文章
    return has_role(current_user, "moderator")


# 评论权限检查
def can_edit_comment(current_user: User, comment_author_id: str) -> bool:
    """
    检查用户是否可以编辑评论
    
    Args:
        current_user: 当前用户对象
        comment_author_id: 评论作者ID
    
    Returns:
        bool: 是否可以编辑
    """
    # 作者可以编辑自己的评论
    if str(current_user.id) == str(comment_author_id):
        return True
    # 管理员和版主可以编辑所有评论
    return has_role(current_user, "moderator")


def can_delete_comment(current_user: User, comment_author_id: str) -> bool:
    """
    检查用户是否可以删除评论
    
    Args:
        current_user: 当前用户对象
        comment_author_id: 评论作者ID
    
    Returns:
        bool: 是否可以删除
    """
    # 作者可以删除自己的评论
    if str(current_user.id) == str(comment_author_id):
        return True
    # 管理员和版主可以删除所有评论
    return has_role(current_user, "moderator")


# 内容审核权限
def can_moderate_content(current_user: User) -> bool:
    """
    检查用户是否可以审核内容
    
    Args:
        current_user: 当前用户对象
    
    Returns:
        bool: 是否可以审核内容
    """
    return has_role(current_user, "moderator")


# 系统管理权限
def can_manage_system(current_user: User) -> bool:
    """
    检查用户是否可以管理系统
    
    Args:
        current_user: 当前用户对象
    
    Returns:
        bool: 是否可以管理系统
    """
    return has_role(current_user, "admin")
