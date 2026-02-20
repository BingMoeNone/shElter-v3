from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from src.database import get_db
from src.models import Tag
from src.schemas import TagResponse, TagCreate, TagUpdate, Pagination
from src.auth.jwt import get_current_user
from src.api.articles import generate_slug

router = APIRouter()


@router.get("/", response_model=dict)
async def list_tags(
    page: int = 1,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    query = db.query(Tag).order_by(Tag.usage_count.desc())
    total = query.count()
    tags = query.offset((page - 1) * limit).limit(limit).all()
    
    return {
        "tags": [TagResponse.model_validate(t) for t in tags],
        "pagination": Pagination(
            page=page,
            limit=limit,
            total_pages=(total + limit - 1) // limit,
            total_items=total
        ).model_dump()
    }


@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag(tag_id: str, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return TagResponse.model_validate(tag)


@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_data: TagCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    slug = generate_slug(tag_data.name)
    existing = db.query(Tag).filter(Tag.slug == slug).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tag with this name already exists"
        )
    
    tag = Tag(name=tag_data.name, slug=slug)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return TagResponse.model_validate(tag)


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(
    tag_id: str,
    tag_data: TagUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    
    slug = generate_slug(tag_data.name)
    existing = db.query(Tag).filter(Tag.slug == slug, Tag.id != tag.id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tag with this name already exists"
        )
    
    tag.name = tag_data.name
    tag.slug = slug
    db.commit()
    db.refresh(tag)
    return TagResponse.model_validate(tag)
