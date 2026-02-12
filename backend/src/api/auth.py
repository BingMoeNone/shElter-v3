from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from src.database import get_db
from src.models import User
from src.schemas import LoginRequest, LoginResponse, UserResponse
from src.auth.jwt import (
    verify_password,
    create_access_token,
    create_refresh_token,
)
from src.config import settings

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated"
        )
    
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user)
    )


@router.post("/logout")
async def logout():
    return {"message": "Successfully logged out"}
