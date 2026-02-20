from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from src.database import get_db
from src.models import Comment, User, Article
from src.schemas import CommentCreate, CommentUpdate, CommentResponse, UserResponse
from src.auth.jwt import get_current_user
from src.auth.permissions import can_edit_comment, can_delete_comment

router = APIRouter()


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    article = db.query(Article).filter(Article.id == comment_data.article_id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    
    if comment_data.parent_id:
        parent = db.query(Comment).filter(Comment.id == comment_data.parent_id).first()
        if not parent:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parent comment not found")
    
    comment = Comment(
        content=comment_data.content,
        author_id=current_user.id,
        article_id=comment_data.article_id,
        parent_id=comment_data.parent_id,
    )
    db.add(comment)
    
    # 鏇存柊鐢ㄦ埛璐＄尞璁℃暟
    current_user.contribution_count += 1
    
    db.commit()
    db.refresh(comment)
    
    return CommentResponse(
        id=comment.id,
        content=comment.content,
        author=UserResponse.model_validate(comment.author),
        article_id=comment.article_id,
        parent_id=comment.parent_id,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
        is_approved=comment.is_approved,
    )


@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: str,
    comment_data: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    
    if not can_edit_comment(current_user, comment.author_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this comment"
        )
    
    comment.content = comment_data.content
    db.commit()
    db.refresh(comment)
    
    return CommentResponse(
        id=comment.id,
        content=comment.content,
        author=UserResponse.model_validate(comment.author),
        article_id=comment.article_id,
        parent_id=comment.parent_id,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
        is_approved=comment.is_approved,
    )


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    
    if not can_delete_comment(current_user, comment.author_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this comment"
        )
    
    db.delete(comment)
    db.commit()
