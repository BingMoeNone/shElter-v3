from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from src.database import get_db
from src.models import Article, Comment, User, AuditLog
from src.schemas import (
    ArticleResponse, CommentResponse, AuditLogResponse,
    ModerationAction, ModerationStatus
)
from src.auth.jwt import get_current_active_user, require_role
from src.core.response import response_wrapper
from src.config import settings
from src.utils.logging import logger

router = APIRouter()


@router.get("/articles", response_model=dict)
async def get_articles_for_moderation(
    status: Optional[ModerationStatus] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user = Depends(require_role(["admin", "moderator"])),
    db: Session = Depends(get_db)
):
    """获取需要审核的文章列表"""
    query = db.query(Article)
    
    if status:
        query = query.filter(Article.moderation_status == status)
    else:
        query = query.filter(Article.moderation_status != ModerationStatus.APPROVED)
    
    # 按创建时间倒序排序
    query = query.order_by(Article.created_at.desc())
    
    total = query.count()
    articles = query.offset(skip).limit(limit).all()
    
    return {
        "articles": articles,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.post("/articles/{article_id}/action", response_model=ArticleResponse)
async def moderate_article(
    article_id: int,
    action: ModerationAction,
    reason: Optional[str] = None,
    current_user = Depends(require_role(["admin", "moderator"])),
    db: Session = Depends(get_db)
):
    """审核文章"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )
    
    # 更新审核状态
    article.moderation_status = action.status
    article.moderated_by = current_user.id
    article.moderation_reason = reason
    
    # 创建审核日志
    audit_log = AuditLog(
        user_id=current_user.id,
        action=f"moderate_article",
        resource_type="article",
        resource_id=article_id,
        details={
            "status": action.status.value,
            "reason": reason
        }
    )
    
    db.add(audit_log)
    db.commit()
    db.refresh(article)
    
    return article


@router.get("/comments", response_model=dict)
async def get_comments_for_moderation(
    status: Optional[ModerationStatus] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user = Depends(require_role(["admin", "moderator"])),
    db: Session = Depends(get_db)
):
    """获取需要审核的评论列表"""
    query = db.query(Comment)
    
    if status:
        query = query.filter(Comment.moderation_status == status)
    else:
        query = query.filter(Comment.moderation_status != ModerationStatus.APPROVED)
    
    # 按创建时间倒序排序
    query = query.order_by(Comment.created_at.desc())
    
    total = query.count()
    comments = query.offset(skip).limit(limit).all()
    
    return {
        "comments": comments,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.post("/comments/{comment_id}/action", response_model=CommentResponse)
async def moderate_comment(
    comment_id: int,
    action: ModerationAction,
    reason: Optional[str] = None,
    current_user = Depends(require_role(["admin", "moderator"])),
    db: Session = Depends(get_db)
):
    """审核评论"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在"
        )
    
    # 更新审核状态
    comment.moderation_status = action.status
    comment.moderated_by = current_user.id
    comment.moderation_reason = reason
    
    # 创建审核日志
    audit_log = AuditLog(
        user_id=current_user.id,
        action=f"moderate_comment",
        resource_type="comment",
        resource_id=comment_id,
        details={
            "status": action.status.value,
            "reason": reason
        }
    )
    
    db.add(audit_log)
    db.commit()
    db.refresh(comment)
    
    return comment


@router.get("/logs", response_model=dict)
async def get_moderation_logs(
    action: Optional[str] = Query(None),
    resource_type: Optional[str] = Query(None),
    user_id: Optional[int] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """获取审核日志"""
    query = db.query(AuditLog)
    
    if action:
        query = query.filter(AuditLog.action == action)
    if resource_type:
        query = query.filter(AuditLog.resource_type == resource_type)
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    if start_date:
        query = query.filter(AuditLog.created_at >= start_date)
    if end_date:
        query = query.filter(AuditLog.created_at <= end_date)
    
    # 按创建时间倒序排序
    query = query.order_by(AuditLog.created_at.desc())
    
    total = query.count()
    logs = query.offset(skip).limit(limit).all()
    
    return {
        "logs": logs,
        "total": total,
        "skip": skip,
        "limit": limit
    }
