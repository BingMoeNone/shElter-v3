from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from src.database import get_db
from src.models import User
from src.schemas import UserRegistration, UserResponse, UserUpdate, UserProfileResponse, Pagination
from src.auth.jwt import get_password_hash, get_current_user

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserRegistration, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists"
        )
    
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


@router.get("/{user_id}", response_model=UserProfileResponse)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserProfileResponse.model_validate(user)


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
