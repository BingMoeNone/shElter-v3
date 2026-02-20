from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from typing import Optional
from datetime import datetime, timedelta

from src.database import get_db
from src.models import User, Article, Comment, Revision, Connection
from src.schemas import UserRegistration, UserResponse, UserUpdate, UserProfileResponse, Pagination, UserContributionStats
from src.auth.jwt import get_password_hash, get_current_user
from src.utils.errors import EmailAlreadyRegisteredError

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserRegistration, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise EmailAlreadyRegisteredError(user_data.email)
    
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        display_name=user_data.display_name or user_data.username,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)


@router.get("/", response_model=dict)
async def list_users(
    page: int = 1,
    limit: int = 20,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(User).filter(User.is_active == True)
    
    if search:
        query = query.filter(
            User.username.ilike(f"%{search}%") | User.display_name.ilike(f"%{search}%")
        )
    
    total = query.count()
    users = query.offset((page - 1) * limit).limit(limit).all()
    
    return {
        "users": [UserResponse.model_validate(u) for u in users],
        "pagination": Pagination(
            page=page,
            limit=limit,
            total_pages=(total + limit - 1) // limit,
            total_items=total
        ).model_dump()
    }


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)


@router.get("/{user_id}", response_model=UserProfileResponse)
async def get_user(user_id: str, db: Session = Depends(get_db), current_user: Optional[User] = Depends(lambda: None)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # 计算贡献统计
    total_articles = db.query(func.count(Article.id)).filter(Article.author_id == user.id).scalar() or 0
    total_comments = db.query(func.count(Comment.id)).filter(Comment.author_id == user.id).scalar() or 0
    total_revisions = db.query(func.count(Revision.id)).filter(Revision.author_id == user.id).scalar() or 0
    total_connections = db.query(func.count(Connection.id)).filter(
        (Connection.follower_id == user.id) | (Connection.followed_id == user.id)
    ).scalar() or 0
    
    # 最近30天的贡献
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_articles = db.query(func.count(Article.id)).filter(
        Article.author_id == user.id,
        Article.created_at >= thirty_days_ago
    ).scalar() or 0
    
    recent_comments = db.query(func.count(Comment.id)).filter(
        Comment.author_id == user.id,
        Comment.created_at >= thirty_days_ago
    ).scalar() or 0
    
    # 构建统计数据
    stats = UserContributionStats(
        total_articles=total_articles,
        total_comments=total_comments,
        total_revisions=total_revisions,
        total_connections=total_connections,
        contribution_count=user.contribution_count,
        recent_articles=recent_articles,
        recent_comments=recent_comments
    )
    
    # 构建响应
    profile_data = {
        **user.__dict__,
        "stats": stats,
        "is_following": False
    }
    
    # 检查当前用户是否关注了该用户
    if current_user and str(current_user.id) != user_id:
        is_following = db.query(Connection).filter(
            Connection.follower_id == current_user.id,
            Connection.followed_id == user.id
        ).first() is not None
        profile_data["is_following"] = is_following
    
    return UserProfileResponse(**profile_data)


@router.get("/{user_id}/stats", response_model=UserContributionStats)
async def get_user_stats(user_id: str, db: Session = Depends(get_db)):
    """获取用户贡献统计"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # 计算贡献统计
    total_articles = db.query(func.count(Article.id)).filter(Article.author_id == user.id).scalar() or 0
    total_comments = db.query(func.count(Comment.id)).filter(Comment.author_id == user.id).scalar() or 0
    total_revisions = db.query(func.count(Revision.id)).filter(Revision.author_id == user.id).scalar() or 0
    total_connections = db.query(func.count(Connection.id)).filter(
        (Connection.follower_id == user.id) | (Connection.followed_id == user.id)
    ).scalar() or 0
    
    # 最近30天的贡献
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_articles = db.query(func.count(Article.id)).filter(
        Article.author_id == user.id,
        Article.created_at >= thirty_days_ago
    ).scalar() or 0
    
    recent_comments = db.query(func.count(Comment.id)).filter(
        Comment.author_id == user.id,
        Comment.created_at >= thirty_days_ago
    ).scalar() or 0
    
    return UserContributionStats(
        total_articles=total_articles,
        total_comments=total_comments,
        total_revisions=total_revisions,
        total_connections=total_connections,
        contribution_count=user.contribution_count,
        recent_articles=recent_articles,
        recent_comments=recent_comments
    )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if str(user.id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this profile"
        )
    
    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)
