import re
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional

from src.database import get_db
from src.models import Article, User, Comment, Tag
from src.schemas import (
    ArticleCreate, ArticleUpdate, ArticleResponse, ArticleListResponse,
    CommentCreate, CommentResponse, RevisionResponse
)
from src.auth.jwt import get_current_active_user
from src.config import settings
from src.utils import ArticleNotFoundError, generate_slug
from src.core.response import response_wrapper
from src.core.security import limiter
from src.utils.logging import logger

router = APIRouter()


@router.get("/", response_model=ArticleListResponse)
async def get_articles(
    title: Optional[str] = Query(None, min_length=1, max_length=200),
    category_id: Optional[int] = Query(None, ge=1),
    tag_id: Optional[int] = Query(None, ge=1),
    author_id: Optional[int] = Query(None, ge=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: Optional[str] = Query("created_at", regex=r"^(created_at|updated_at|views|likes)$"),
    sort_order: Optional[str] = Query("desc", regex=r"^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """获取文章列表"""
    query = db.query(Article)
    
    # 应用过滤条件
    if title:
        query = query.filter(Article.title.ilike(f"%{title}%"))
    if category_id:
        query = query.filter(Article.category_id == category_id)
    if tag_id:
        query = query.filter(Article.tags.any(id=tag_id))
    if author_id:
        query = query.filter(Article.author_id == author_id)
    
    # 应用排序
    order_by = getattr(Article, sort_by)
    if sort_order == "desc":
        order_by = order_by.desc()
    query = query.order_by(order_by)
    
    # 获取总数
    total = query.count()
    
    # 分页
    articles = query.offset(skip).limit(limit).all()
    
    return ArticleListResponse(
        items=articles,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(
    article_id: int,
    current_user: Optional[User] = Depends(lambda: None),
    db: Session = Depends(get_db)
):
    """获取文章详情"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise ArticleNotFoundError(article_id)
    
    # 增加文章浏览量
    article.views += 1
    db.commit()
    
    return article


@router.post("/", response_model=ArticleResponse)
async def create_article(
    article: ArticleCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建新文章"""
    new_article = Article(
        title=article.title,
        content=article.content,
        category_id=article.category_id,
        author_id=current_user.id
    )
    
    # 添加标签
    if article.tags:
        for tag_id in article.tags:
            tag = db.query(Tag).filter(Tag.id == tag_id).first()
            if tag:
                new_article.tags.append(tag)
    
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    
    return new_article


@router.put("/{article_id}", response_model=ArticleResponse)
async def update_article(
    article_id: int,
    article_update: ArticleUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新文章"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise ArticleNotFoundError(article_id)
    
    # 检查权限
    if article.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限修改该文章"
        )
    
    # 更新文章内容
    for field, value in article_update.dict(exclude_unset=True).items():
        setattr(article, field, value)
    
    # 更新标签
    if article_update.tags is not None:
        # 清空现有标签
        article.tags.clear()
        # 添加新标签
        for tag_id in article_update.tags:
            tag = db.query(Tag).filter(Tag.id == tag_id).first()
            if tag:
                article.tags.append(tag)
    
    db.commit()
    db.refresh(article)
    
    return article


@router.delete("/{article_id}")
async def delete_article(
    article_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """删除文章"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise ArticleNotFoundError(article_id)
    
    # 检查权限
    if article.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限删除该文章"
        )
    
    db.delete(article)
    db.commit()
    
    return response_wrapper.success(message=f"文章 {article_id} 已成功删除")


@router.post("/{article_id}/comments", response_model=CommentResponse)
async def create_article_comment(
    article_id: int,
    comment: CommentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """给文章添加评论"""
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


@router.get("/{article_id}/comments", response_model=List[CommentResponse])
async def get_article_comments(
    article_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """获取文章评论"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise ArticleNotFoundError(article_id)
    
    comments = db.query(Comment).filter(
        Comment.article_id == article_id
    ).order_by(Comment.created_at.desc()).offset(skip).limit(limit).all()
    
    return comments


@router.get("/{article_id}/revisions", response_model=List[RevisionResponse])
async def get_article_revisions(
    article_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """获取文章修订历史"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise ArticleNotFoundError(article_id)
    
    revisions = db.query(Article.revisions).filter(
        Article.id == article_id
    ).order_by(Article.revisions.c.created_at.desc()).offset(skip).limit(limit).all()
    
    return revisions


@router.post("/{article_id}/like")
async def like_article(
    article_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """点赞文章"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise ArticleNotFoundError(article_id)
    
    # 检查是否已经点赞
    if article.likes.filter(User.id == current_user.id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="已经点赞过该文章"
        )
    
    # 添加点赞
    article.likes.append(current_user)
    db.commit()
    
    return response_wrapper.success(message=f"成功点赞文章 {article_id}")


@router.post("/{article_id}/unlike")
async def unlike_article(
    article_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """取消点赞文章"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise ArticleNotFoundError(article_id)
    
    # 检查是否已经点赞
    like = article.likes.filter(User.id == current_user.id).first()
    if not like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="没有点赞过该文章"
        )
    
    # 移除点赞
    article.likes.remove(current_user)
    db.commit()
    
    return response_wrapper.success(message=f"成功取消点赞文章 {article_id}")
