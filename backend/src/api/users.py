from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta

from src.database import get_db
from src.auth.jwt import get_current_active_user
from src.models.user import User
from src.models.article import Article
from src.models.comment import Comment
from src.schemas import (
    UserResponse, UserUpdate, UserProfileResponse, UserContributionStats
)
from src.utils.errors import UserNotFoundError, InvalidCredentialsError

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """获取当前用户信息"""
    return current_user


@router.get("/{username}", response_model=UserProfileResponse)
async def get_user_profile(
    username: str,
    current_user: Optional[User] = Depends(lambda: None),
    db: Session = Depends(get_db)
):
    """获取用户个人资料"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise UserNotFoundError(username)
    
    # 检查当前用户是否关注该用户
    is_following = False
    if current_user:
        is_following = user.followers.filter(User.id == current_user.id).first() is not None
    
    # 计算最近30天的时间点
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    # 统计最近30天创建的文章数量
    recent_articles = len([article for article in user.articles if article.created_at >= thirty_days_ago])
    
    # 统计最近30天创建的评论数量
    recent_comments = len([comment for comment in user.comments if comment.created_at >= thirty_days_ago])
    
    # 计算用户贡献统计
    stats = UserContributionStats(
        total_articles=len(user.articles),
        total_comments=len(user.comments),
        total_revisions=sum(len(article.revisions) for article in user.articles),
        total_connections=len(user.followers) + len(user.following),
        contribution_count=len(user.articles) + len(user.comments) + sum(len(article.revisions) for article in user.articles),
        recent_articles=recent_articles,
        recent_comments=recent_comments
    )
    
    return UserProfileResponse(
        id=str(user.id),
        username=user.username,
        display_name=user.display_name,
        bio=user.bio,
        avatar_url=user.avatar_url,
        level=user.level,
        created_at=user.created_at,
        contribution_count=stats.contribution_count,
        is_following=is_following,
        stats=stats
    )


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新当前用户信息"""
    # 更新用户信息
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return current_user


@router.get("/stats/{username}", response_model=UserContributionStats)
async def get_user_contribution_stats(
    username: str,
    db: Session = Depends(get_db)
):
    """获取用户贡献统计"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise UserNotFoundError(username)
    
    # 计算最近30天的时间点
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    # 统计最近30天创建的文章数量
    recent_articles = len([article for article in user.articles if article.created_at >= thirty_days_ago])
    
    # 统计最近30天创建的评论数量
    recent_comments = len([comment for comment in user.comments if comment.created_at >= thirty_days_ago])
    
    stats = UserContributionStats(
        total_articles=len(user.articles),
        total_comments=len(user.comments),
        total_revisions=sum(len(article.revisions) for article in user.articles),
        total_connections=len(user.followers) + len(user.following),
        contribution_count=len(user.articles) + len(user.comments) + sum(len(article.revisions) for article in user.articles),
        recent_articles=recent_articles,
        recent_comments=recent_comments
    )
    
    return stats


@router.get("/search/{query}", response_model=List[UserResponse])
async def search_users(
    query: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """搜索用户"""
    users = db.query(User).filter(
        User.username.ilike(f"%{query}%") | 
        User.display_name.ilike(f"%{query}%")
    ).offset(skip).limit(limit).all()
    
    return users


@router.post("/follow/{username}")
async def follow_user(
    username: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """关注用户"""
    user_to_follow = db.query(User).filter(User.username == username).first()
    if not user_to_follow:
        raise UserNotFoundError(username)
    
    if current_user.id == user_to_follow.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能关注自己"
        )
    
    # 检查是否已经关注
    if user_to_follow.followers.filter(User.id == current_user.id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="已经关注了该用户"
        )
    
    # 添加关注关系
    current_user.following.append(user_to_follow)
    db.commit()
    
    return {"message": f"成功关注 {username}"}


@router.post("/unfollow/{username}")
async def unfollow_user(
    username: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """取消关注用户"""
    user_to_unfollow = db.query(User).filter(User.username == username).first()
    if not user_to_unfollow:
        raise UserNotFoundError(username)
    
    # 检查是否已经关注
    following = user_to_unfollow.followers.filter(User.id == current_user.id).first()
    if not following:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="没有关注该用户"
        )
    
    # 移除关注关系
    current_user.following.remove(user_to_unfollow)
    db.commit()
    
    return {"message": f"成功取消关注 {username}"}


@router.get("/followers/{username}", response_model=List[UserResponse])
async def get_user_followers(
    username: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """获取用户的粉丝列表"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise UserNotFoundError(username)
    
    followers = user.followers.offset(skip).limit(limit).all()
    return followers


@router.get("/following/{username}", response_model=List[UserResponse])
async def get_user_following(
    username: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """获取用户关注的用户列表"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise UserNotFoundError(username)
    
    following = user.following.offset(skip).limit(limit).all()
    return following
