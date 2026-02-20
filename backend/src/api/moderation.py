from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Optional, List

from src.database import get_db
from src.models import Article, Comment, User
from src.schemas import ArticleResponse, CommentResponse, Pagination
from src.auth.jwt import get_current_user, require_role

router = APIRouter()


# 浣跨敤鏂扮殑鏉冮檺绯荤粺
def require_moderator():
    return require_role(["moderator"])


@router.get("/articles/pending", response_model=dict)
async def get_pending_articles(
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db),
    moderator: User = Depends(require_moderator()),
):
    """鑾峰彇寰呭鏍哥殑鏂囩珷"""
    query = db.query(Article).filter(Article.is_approved == False)
    
    total = query.count()
    articles = query.order_by(desc(Article.created_at)).offset((page - 1) * limit).limit(limit).all()
    
    return {
        "articles": [ArticleResponse.model_validate(a) for a in articles],
        "pagination": Pagination(
            page=page,
            limit=limit,
            total_pages=(total + limit - 1) // limit,
            total_items=total
        ).model_dump()
    }


@router.put("/articles/{article_id}/approve", response_model=ArticleResponse)
async def approve_article(
    article_id: str,
    db: Session = Depends(get_db),
    moderator: User = Depends(require_moderator()),
):
    """瀹℃牳閫氳繃鏂囩珷"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="鏂囩珷涓嶅瓨鍦?)
    
    article.is_approved = True
    db.commit()
    db.refresh(article)
    
    return ArticleResponse.model_validate(article)


@router.put("/articles/{article_id}/reject", response_model=ArticleResponse)
async def reject_article(
    article_id: str,
    db: Session = Depends(get_db),
    moderator: User = Depends(require_moderator()),
):
    """鎷掔粷鏂囩珷瀹℃牳"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="鏂囩珷涓嶅瓨鍦?)
    
    article.is_approved = False
    article.status = "draft"
    db.commit()
    db.refresh(article)
    
    return ArticleResponse.model_validate(article)


@router.get("/comments/pending", response_model=dict)
async def get_pending_comments(
    page: int = 1,
    limit: int = 20,
    article_id: Optional[str] = None,
    db: Session = Depends(get_db),
    moderator: User = Depends(require_moderator()),
):
    """鑾峰彇寰呭鏍哥殑璇勮"""
    query = db.query(Comment).filter(Comment.is_approved == False)
    
    if article_id:
        query = query.filter(Comment.article_id == article_id)
    
    total = query.count()
    comments = query.order_by(desc(Comment.created_at)).offset((page - 1) * limit).limit(limit).all()
    
    return {
        "comments": [CommentResponse.model_validate(c) for c in comments],
        "pagination": Pagination(
            page=page,
            limit=limit,
            total_pages=(total + limit - 1) // limit,
            total_items=total
        ).model_dump()
    }


@router.put("/comments/{comment_id}/approve", response_model=CommentResponse)
async def approve_comment(
    comment_id: str,
    db: Session = Depends(get_db),
    moderator: User = Depends(require_moderator()),
):
    """瀹℃牳閫氳繃璇勮"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="璇勮涓嶅瓨鍦?)
    
    comment.is_approved = True
    db.commit()
    db.refresh(comment)
    
    return CommentResponse.model_validate(comment)


@router.put("/comments/{comment_id}/reject", response_model=CommentResponse)
async def reject_comment(
    comment_id: str,
    db: Session = Depends(get_db),
    moderator: User = Depends(require_moderator()),
):
    """鎷掔粷璇勮瀹℃牳"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="璇勮涓嶅瓨鍦?)
    
    comment.is_approved = False
    db.commit()
    db.refresh(comment)
    
    return CommentResponse.model_validate(comment)


@router.put("/comments/{comment_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: str,
    db: Session = Depends(get_db),
    moderator: User = Depends(require_moderator()),
):
    """鍒犻櫎杩濊璇勮"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="璇勮涓嶅瓨鍦?)
    
    db.delete(comment)
    db.commit()


@router.put("/articles/{article_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    article_id: str,
    db: Session = Depends(get_db),
    moderator: User = Depends(require_moderator()),
):
    """鍒犻櫎杩濊鏂囩珷"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="鏂囩珷涓嶅瓨鍦?)
    
    db.delete(article)
    db.commit()


@router.get("/stats", response_model=dict)
async def get_moderation_stats(
    db: Session = Depends(get_db),
    moderator: User = Depends(require_moderator()),
):
    """鑾峰彇瀹℃牳缁熻淇℃伅"""
    # 寰呭鏍告枃绔犳暟閲?    pending_articles = db.query(func.count(Article.id)).filter(Article.is_approved == False).scalar() or 0
    
    # 寰呭鏍歌瘎璁烘暟閲?    pending_comments = db.query(func.count(Comment.id)).filter(Comment.is_approved == False).scalar() or 0
    
    # 宸插鏍告枃绔犳暟閲?    approved_articles = db.query(func.count(Article.id)).filter(Article.is_approved == True).scalar() or 0
    
    # 宸插鏍歌瘎璁烘暟閲?    approved_comments = db.query(func.count(Comment.id)).filter(Comment.is_approved == True).scalar() or 0
    
    return {
        "pending_articles": pending_articles,
        "pending_comments": pending_comments,
        "approved_articles": approved_articles,
        "approved_comments": approved_comments,
    }
