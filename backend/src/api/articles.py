import re
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID

from src.database import get_db
from src.models import Article, User, Category, Tag, Revision, article_categories, article_tags
from src.schemas import (
    ArticleCreate,
    ArticleUpdate,
    ArticleResponse,
    ArticleListResponse,
    Pagination,
    CategoryResponse,
    TagResponse,
    UserResponse,
)
from src.auth.jwt import get_current_user
from src.auth.permissions import can_edit_article, can_delete_article

router = APIRouter()


def generate_slug(title: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", title.lower())
    slug = re.sub(r"[\s_-]+", "-", slug)
    return slug.strip("-")


@router.post("/", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_article(
    article_data: ArticleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    slug = generate_slug(article_data.title)
    existing = db.query(Article).filter(Article.slug == slug).first()
    if existing:
        slug = f"{slug}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    
    article = Article(
        title=article_data.title,
        slug=slug,
        content=article_data.content,
        summary=article_data.summary,
        status=article_data.status,
        author_id=current_user.id,
    )
    
    if article_data.category_ids:
        categories = db.query(Category).filter(Category.id.in_(article_data.category_ids)).all()
        article.categories = categories
    
    if article_data.tag_names:
        for tag_name in article_data.tag_names:
            tag = db.query(Tag).filter(Tag.name.ilike(tag_name)).first()
            if not tag:
                tag = Tag(name=tag_name, slug=generate_slug(tag_name))
                db.add(tag)
            article.tags.append(tag)
    
    db.add(article)
    db.commit()
    db.refresh(article)
    
    # 鏇存柊鐢ㄦ埛璐＄尞璁℃暟
    current_user.contribution_count += 1
    
    revision = Revision(
        article_id=article.id,
        author_id=current_user.id,
        title=article.title,
        content=article.content,
        revision_number=1,
        change_summary="Initial version",
    )
    db.add(revision)
    db.commit()
    
    return ArticleResponse(
        id=article.id,
        title=article.title,
        slug=article.slug,
        content=article.content,
        summary=article.summary,
        status=article.status,
        author=UserResponse.model_validate(article.author),
        published_at=article.published_at,
        created_at=article.created_at,
        updated_at=article.updated_at,
        view_count=article.view_count,
        is_featured=article.is_featured,
        categories=[CategoryResponse.model_validate(c) for c in article.categories],
        tags=[TagResponse.model_validate(t) for t in article.tags],
    )


@router.get("/", response_model=dict)
async def list_articles(
    page: int = 1,
    limit: int = 20,
    status: Optional[str] = None,
    category: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Article)
    
    if status:
        query = query.filter(Article.status == status)
    else:
        query = query.filter(Article.status == "published")
    
    if category:
        query = query.join(Article.categories).filter(Category.slug == category)
    
    if tag:
        query = query.join(Article.tags).filter(Tag.slug == tag)
    
    if search:
        query = query.filter(
            Article.title.ilike(f"%{search}%") | Article.content.ilike(f"%{search}%")
        )
    
    total = query.count()
    articles = query.order_by(Article.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    
    return {
        "articles": [
            ArticleResponse(
                id=a.id,
                title=a.title,
                slug=a.slug,
                content=a.content,
                summary=a.summary,
                status=a.status,
                author=UserResponse.model_validate(a.author),
                published_at=a.published_at,
                created_at=a.created_at,
                updated_at=a.updated_at,
                view_count=a.view_count,
                is_featured=a.is_featured,
                categories=[CategoryResponse.model_validate(c) for c in a.categories],
                tags=[TagResponse.model_validate(t) for t in a.tags],
            ) for a in articles
        ],
        "pagination": Pagination(
            page=page,
            limit=limit,
            total_pages=(total + limit - 1) // limit,
            total_items=total
        ).model_dump()
    }


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: str, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    
    article.view_count += 1
    db.commit()
    
    return ArticleResponse(
        id=article.id,
        title=article.title,
        slug=article.slug,
        content=article.content,
        summary=article.summary,
        status=article.status,
        author=UserResponse.model_validate(article.author),
        published_at=article.published_at,
        created_at=article.created_at,
        updated_at=article.updated_at,
        view_count=article.view_count,
        is_featured=article.is_featured,
        categories=[CategoryResponse.model_validate(c) for c in article.categories],
        tags=[TagResponse.model_validate(t) for t in article.tags],
    )


@router.put("/{article_id}", response_model=ArticleResponse)
async def update_article(
    article_id: str,
    article_data: ArticleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    
    if not can_edit_article(current_user, article.author_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this article"
        )
    
    update_data = article_data.model_dump(exclude_unset=True)
    
    if article_data.category_ids is not None:
        categories = db.query(Category).filter(Category.id.in_(article_data.category_ids)).all()
        article.categories = categories
    
    if article_data.tag_names is not None:
        article.tags = []
        for tag_name in article_data.tag_names:
            tag = db.query(Tag).filter(Tag.name.ilike(tag_name)).first()
            if not tag:
                tag = Tag(name=tag_name, slug=generate_slug(tag_name))
                db.add(tag)
            article.tags.append(tag)
    
    for key, value in update_data.items():
        if key not in ["category_ids", "tag_names"]:
            setattr(article, key, value)
    
    latest_revision = db.query(Revision).filter(
        Revision.article_id == article.id
    ).order_by(Revision.revision_number.desc()).first()
    
    revision_number = (latest_revision.revision_number + 1) if latest_revision else 1
    revision = Revision(
        article_id=article.id,
        author_id=current_user.id,
        title=article.title,
        content=article.content,
        revision_number=revision_number,
        change_summary=f"Updated article",
    )
    db.add(revision)
    
    # 鏇存柊鐢ㄦ埛璐＄尞璁℃暟
    current_user.contribution_count += 1
    
    db.commit()
    db.refresh(article)
    
    return ArticleResponse(
        id=article.id,
        title=article.title,
        slug=article.slug,
        content=article.content,
        summary=article.summary,
        status=article.status,
        author=UserResponse.model_validate(article.author),
        published_at=article.published_at,
        created_at=article.created_at,
        updated_at=article.updated_at,
        view_count=article.view_count,
        is_featured=article.is_featured,
        categories=[CategoryResponse.model_validate(c) for c in article.categories],
        tags=[TagResponse.model_validate(t) for t in article.tags],
    )


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    article_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    
    if not can_delete_article(current_user, article.author_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this article"
        )
    
    article.status = "archived"
    db.commit()


@router.post("/{article_id}/publish", response_model=ArticleResponse)
async def publish_article(
    article_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    
    if str(article.author_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to publish this article"
        )
    
    if len(article.content) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Article content must be at least 10 characters"
        )
    
    article.status = "published"
    article.published_at = datetime.utcnow()
    db.commit()
    db.refresh(article)
    
    return ArticleResponse(
        id=article.id,
        title=article.title,
        slug=article.slug,
        content=article.content,
        summary=article.summary,
        status=article.status,
        author=UserResponse.model_validate(article.author),
        published_at=article.published_at,
        created_at=article.created_at,
        updated_at=article.updated_at,
        view_count=article.view_count,
        is_featured=article.is_featured,
        categories=[CategoryResponse.model_validate(c) for c in article.categories],
        tags=[TagResponse.model_validate(t) for t in article.tags],
    )


@router.get("/{article_id}/revisions", response_model=dict)
async def get_article_revisions(article_id: str, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    
    revisions = db.query(Revision).filter(
        Revision.article_id == article.id
    ).order_by(Revision.revision_number.desc()).all()
    
    from src.schemas import RevisionResponse
    return {
        "revisions": [
            RevisionResponse(
                id=r.id,
                article_id=r.article_id,
                author=UserResponse.model_validate(r.author),
                title=r.title,
                content=r.content,
                change_summary=r.change_summary,
                revision_number=r.revision_number,
                created_at=r.created_at,
            ) for r in revisions
        ]
    }
