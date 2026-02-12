from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from src.database import get_db
from src.models import Category
from src.schemas import CategoryResponse, CategoryCreate, CategoryUpdate, Pagination
from src.auth.jwt import get_current_user, require_role
from src.api.articles import generate_slug

router = APIRouter()


@router.get("/", response_model=dict)
async def list_categories(
    page: int = 1,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    query = db.query(Category)
    total = query.count()
    categories = query.offset((page - 1) * limit).limit(limit).all()
    
    return {
        "categories": [CategoryResponse.model_validate(c) for c in categories],
        "pagination": Pagination(
            page=page,
            limit=limit,
            total_pages=(total + limit - 1) // limit,
            total_items=total
        ).model_dump()
    }


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: str, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return CategoryResponse.model_validate(category)


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["admin", "moderator"])),
):
    slug = generate_slug(category_data.name)
    existing = db.query(Category).filter(Category.slug == slug).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category with this name already exists"
        )
    
    category = Category(
        name=category_data.name,
        slug=slug,
        description=category_data.description,
        parent_id=category_data.parent_id,
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return CategoryResponse.model_validate(category)


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: str,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["admin", "moderator"])),
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    update_data = category_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)
    
    db.commit()
    db.refresh(category)
    return CategoryResponse.model_validate(category)
