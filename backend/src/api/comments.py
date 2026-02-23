from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.models import Comment, Article
from src.schemas import CommentCreate, CommentResponse, CommentUpdate
from src.auth.jwt import get_current_active_user
from src.utils.errors import ArticleNotFoundError
from src.core.response import response_wrapper

router = APIRouter()


@router.get("/", response_model=List[CommentResponse])
async def get_comments(
    article_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """获取文章评论"""
    # 检查文章是否存在
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise ArticleNotFoundError(article_id)
    
    comments = db.query(Comment).filter(
        Comment.article_id == article_id
    ).order_by(Comment.created_at.desc()).offset(skip).limit(limit).all()
    
    return comments


@router.post("/", response_model=CommentResponse)
async def create_comment(
    article_id: int,
    comment: CommentCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建评论"""
    # 检查文章是否存在
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise ArticleNotFoundError(article_id)
    
    new_comment = Comment(
        content=comment.content,
        article_id=article_id,
        author_id=current_user.id
    )
    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return new_comment


@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment(
    comment_id: int,
    db: Session = Depends(get_db)
):
    """获取单个评论"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在"
        )
    
    return comment


@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    comment_update: CommentUpdate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新评论"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在"
        )
    
    # 检查权限
    if comment.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限修改该评论"
        )
    
    # 更新评论内容
    for field, value in comment_update.dict(exclude_unset=True).items():
        setattr(comment, field, value)
    
    db.commit()
    db.refresh(comment)
    
    return comment


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """删除评论"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在"
        )
    
    # 检查权限
    if comment.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限删除该评论"
        )
    
    db.delete(comment)
    db.commit()
    
    return response_wrapper.success(message=f"评论 {comment_id} 已成功删除")
