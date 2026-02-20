from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from src.database import get_db
from src.models import Article, Category, Tag
from src.schemas import ArticleResponse, Pagination, CategoryResponse, TagResponse, UserResponse

router = APIRouter()


@router.get("/", response_model=dict)
async def search_articles(
    q: str = Query(..., min_length=1),
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    query = db.query(Article).filter(
        Article.status == "published",
        Article.title.ilike(f"%{q}%") | Article.content.ilike(f"%{q}%")
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
        ).model_dump(),
        "total": total,
    }
