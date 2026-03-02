# -*- coding: utf-8 -*-
"""
认证相关API接口
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from datetime import timedelta
import re

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

# 密码复杂度正则表达式
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

router = APIRouter()


@router.post("/login")
@limiter.limit("10/minute")
async def login(
    request: Request,
    response: Response,
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    用户登录接口

    Args:
        request: 请求对象
        response: 响应对象
        login_data: 登录数据（包含username, email, password）
        db: 数据库会话

    Returns:
        登录结果，包含令牌和用户信息
    """
    user = db.query(User).filter(User.email == login_data.email).first()

    password_valid = False
    if user:
        password_valid = verify_password(login_data.password, user.password_hash)

    if not user or not password_valid:
        logger.warning(f"Login failed for email: {login_data.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "用户名或密码错误", "error_code": "INVALID_CREDENTIALS"},
        )

    if login_data.username and user.username != login_data.username:
        logger.warning(f"Username mismatch for email: {login_data.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "用户名或密码错误", "error_code": "INVALID_CREDENTIALS"},
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
        message="登录成功",
    )


@router.post("/register")
@limiter.limit("5/minute")
async def register(
    request: Request, response: Response, user_data: dict, db: Session = Depends(get_db)
):
    """
    用户注册接口

    Args:
        request: 请求对象
        response: 响应对象
        user_data: 用户数据（包含email, username, password）
        db: 数据库会话

    Returns:
        注册结果，包含用户信息和令牌
    """
    email = user_data.get("email")
    username = user_data.get("username")
    password = user_data.get("password")

    if not email or not username or not password:
        return response_wrapper.error(
            message="缺少必要参数", error_code="MISSING_PARAMS", status_code=400
        )

    # 验证密码复杂度
    if not re.match(PASSWORD_REGEX, password):
        return response_wrapper.error(
            message="密码必须包含至少一个大写字母、一个小写字母，一个数字和一个特殊字符",
            error_code="INVALID_PASSWORD",
            status_code=400
        )

    existing_user = (
        db.query(User)
        .filter((User.email == email) | (User.username == username))
        .first()
    )

    if existing_user:
        if existing_user.email == email:
            return response_wrapper.error(
                message="邮箱已被注册", error_code="EMAIL_EXISTS", status_code=400
            )
        else:
            return response_wrapper.error(
                message="用户名已被使用", error_code="USERNAME_EXISTS", status_code=400
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
        message="注册成功",
    )


@router.post("/refresh")
@limiter.limit("10/minute")
async def refresh_token(
    request: Request,
    response: Response,
    refresh_data: dict,
    db: Session = Depends(get_db),
):
    """
    刷新访问令牌

    Args:
        request: 请求对象
        response: 响应对象
        refresh_data: 刷新令牌数据（包含refresh_token）
        db: 数据库会话

    Returns:
        新的访问令牌
    """
    refresh_token_value = refresh_data.get("refresh_token")

    if not refresh_token_value:
        return response_wrapper.error(
            message="缺少刷新令牌", error_code="MISSING_TOKEN", status_code=400
        )

    payload = decode_token(refresh_token_value, token_type="refresh")

    if not payload:
        return response_wrapper.error(
            message="无效的刷新令牌", error_code="INVALID_TOKEN", status_code=401
        )

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()

    if not user or not user.is_active:
        return response_wrapper.error(
            message="用户不存在或已禁用", error_code="USER_NOT_FOUND", status_code=404
        )

    access_token = create_access_token(data={"sub": str(user.id)})

    return response_wrapper.success(
        data={"access_token": access_token, "token_type": "bearer"},
        message="令牌刷新成功",
    )


@router.get("/me")
async def get_current_user_info(current_user: User = Depends(lambda: None)):
    """
    获取当前用户信息

    Args:
        current_user: 当前登录用户

    Returns:
        当前用户信息
    """
    if not current_user:
        return response_wrapper.error(
            message="未授权访问", error_code="UNAUTHORIZED", status_code=401
        )

    return response_wrapper.success(
        data={
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "role": current_user.role,
            "is_active": current_user.is_active,
        },
        message="获取成功",
    )


@router.post("/logout")
async def logout(response: Response):
    """
    用户登出

    Args:
        response: 响应对象

    Returns:
        登出结果
    """
    response.delete_cookie(key="access_token")
    return response_wrapper.success(message="登出成功")
