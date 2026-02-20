from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from datetime import timedelta

from src.database import get_db
from src.models import User
from src.schemas import LoginRequest, LoginResponse, UserResponse
from src.auth.jwt import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from src.config import settings
from src.utils.errors import (
    InvalidCredentialsError,
    UsernameEmailMismatchError,
    AccountDeactivatedError,
)
from src.core.response import response_wrapper
from src.core.security import limiter
from src.utils.logging import logger

router = APIRouter()


@router.post("/login")
@limiter.limit("10/minute")
async def login(
    request: Request,
    response: Response,
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    """鐢ㄦ埛鐧诲綍 - 甯ate Limiting"""
    user = db.query(User).filter(User.email == login_data.email).first()

    password_valid = False
    if user:
        password_valid = verify_password(login_data.password, user.password_hash)

    if not user or not password_valid:
        logger.warning(f"Login failed for email: {login_data.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "鐢ㄦ埛鍚嶆垨瀵嗙爜閿欒", "error_code": "INVALID_CREDENTIALS"},
        )

    if user.username != login_data.username:
        logger.warning(f"Username mismatch for email: {login_data.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "鐢ㄦ埛鍚嶆垨瀵嗙爜閿欒", "error_code": "INVALID_CREDENTIALS"},
        )

    if not user.is_active:
        logger.warning(f"Login attempt for deactivated user: {login_data.email}")
        raise AccountDeactivatedError()

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    logger.info(f"User logged in: {user.email}, user_id: {user.id}")

    return response_wrapper.success(
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
            },
        },
        message="鐧诲綍鎴愬姛",
    )


@router.post("/register")
@limiter.limit("5/minute")
async def register(
    request: Request, response: Response, user_data: dict, db: Session = Depends(get_db)
):
    """鐢ㄦ埛娉ㄥ唽 - 甯ate Limiting"""
    email = user_data.get("email")
    username = user_data.get("username")
    password = user_data.get("password")

    if not email or not username or not password:
        return response_wrapper.error(
            message="缂哄皯蹇呰鍙傛暟", error_code="MISSING_PARAMS", status_code=400
        )

    existing_user = (
        db.query(User)
        .filter((User.email == email) | (User.username == username))
        .first()
    )

    if existing_user:
        if existing_user.email == email:
            return response_wrapper.error(
                message="閭宸茶娉ㄥ唽", error_code="EMAIL_EXISTS", status_code=400
            )
        else:
            return response_wrapper.error(
                message="鐢ㄦ埛鍚嶅凡琚娇鐢?, error_code="USERNAME_EXISTS", status_code=400
            )

    from src.auth.jwt import get_password_hash

    new_user = User(
        email=email,
        username=username,
        password_hash=get_password_hash(password),
        role="user",
        is_active=True,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"New user registered: {email}, user_id: {new_user.id}")

    access_token = create_access_token(data={"sub": str(new_user.id)})

    return response_wrapper.success(
        data={
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "access_token": access_token,
            "token_type": "bearer",
        },
        message="娉ㄥ唽鎴愬姛",
    )


@router.post("/refresh")
@limiter.limit("10/minute")
async def refresh_token(
    request: Request,
    response: Response,
    refresh_data: dict,
    db: Session = Depends(get_db),
):
    """鍒锋柊璁块棶浠ょ墝"""
    refresh_token_value = refresh_data.get("refresh_token")

    if not refresh_token_value:
        return response_wrapper.error(
            message="缂哄皯鍒锋柊浠ょ墝", error_code="MISSING_TOKEN", status_code=400
        )

    payload = decode_token(refresh_token_value, token_type="refresh")

    if not payload:
        return response_wrapper.error(
            message="鏃犳晥鐨勫埛鏂颁护鐗?, error_code="INVALID_TOKEN", status_code=401
        )

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user or not user.is_active:
        return response_wrapper.error(
            message="鐢ㄦ埛涓嶅瓨鍦ㄦ垨宸茬鐢?, error_code="USER_NOT_FOUND", status_code=404
        )

    access_token = create_access_token(data={"sub": str(user.id)})

    return response_wrapper.success(
        data={"access_token": access_token, "token_type": "bearer"},
        message="浠ょ墝鍒锋柊鎴愬姛",
    )


@router.get("/me")
async def get_current_user_info(current_user: User = Depends(lambda: None)):
    """鑾峰彇褰撳墠鐢ㄦ埛淇℃伅"""
    if not current_user:
        return response_wrapper.error(
            message="鏈巿鏉冭闂?, error_code="UNAUTHORIZED", status_code=401
        )

    return response_wrapper.success(
        data={
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "role": current_user.role,
            "is_active": current_user.is_active,
        },
        message="鑾峰彇鎴愬姛",
    )


@router.post("/logout")
async def logout(response: Response):
    """鐢ㄦ埛鐧诲嚭"""
    response.delete_cookie(key="access_token")
    return response_wrapper.success(message="鐧诲嚭鎴愬姛")
