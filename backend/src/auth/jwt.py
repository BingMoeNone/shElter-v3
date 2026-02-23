from datetime import datetime, timedelta
from typing import Optional
import os

import bcrypt
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.config import settings
from src.database import get_db
from src.models import User

security = HTTPBearer()


def _read_key_file(file_path: str) -> str:
    """璇诲彇瀵嗛挜鏂囦欢"""
    try:
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        fixed_path = os.path.join(current_dir, file_path.replace('/', os.sep))
        
        with open(fixed_path, "r") as f:
            key_content = f.read()
        
        if not key_content:
            raise ValueError(f"Key file is empty: {file_path}")
        
        return key_content
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Key file not found: {file_path}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reading key file: {str(e)}"
        )


def _get_private_key() -> str:
    """鑾峰彇RSA绉侀挜"""
    if settings.ALGORITHM.startswith("HS"):
        return settings.SECRET_KEY
    return _read_key_file(settings.PRIVATE_KEY_PATH)


def _get_public_key() -> str:
    """鑾峰彇RSA鍏挜"""
    if settings.ALGORITHM.startswith("HS"):
        return settings.SECRET_KEY
    return _read_key_file(settings.PUBLIC_KEY_PATH)


def _get_signing_key() -> str:
    """鑾峰彇绛惧悕瀵嗛挜"""
    algorithm = settings.ALGORITHM.upper()
    if algorithm.startswith("HS"):
        if not settings.SECRET_KEY:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Missing SECRET_KEY for HS* JWT algorithm"
            )
        return settings.SECRET_KEY
    return _get_private_key()


def _get_verification_key() -> str:
    """鑾峰彇楠岃瘉瀵嗛挜"""
    algorithm = settings.ALGORITHM.upper()
    if algorithm.startswith("HS"):
        if not settings.SECRET_KEY:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Missing SECRET_KEY for HS* JWT algorithm"
            )
        return settings.SECRET_KEY
    return _get_public_key()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """楠岃瘉瀵嗙爜"""
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def get_password_hash(password: str) -> str:
    """鐢熸垚瀵嗙爜鍝堝笇"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """鍒涘缓璁块棶浠ょ墝"""
    to_encode = data.copy()
    now = datetime.utcnow()
    
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": now,
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(
        to_encode, 
        _get_signing_key(), 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """鍒涘缓鍒锋柊浠ょ墝"""
    to_encode = data.copy()
    now = datetime.utcnow()
    
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "iat": now,
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(
        to_encode, 
        _get_signing_key(), 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str, token_type: str = "access") -> Optional[dict]:
    """瑙ｇ爜浠ょ墝"""
    try:
        payload = jwt.decode(
            token,
            _get_verification_key(),
            algorithms=[settings.ALGORITHM],
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_iat": True,
                "require_exp": True,
                "require_iat": True,
                "require": ["exp", "iat", "type", "sub"]
            }
        )
        
        if payload.get("type") != token_type:
            return None
        
        return payload
    except JWTError:
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """鑾峰彇褰撳墠鐢ㄦ埛"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="鏃犳晥鐨勮闂护鐗?",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    payload = decode_token(token, token_type="access")
    
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="鐢ㄦ埛宸茶绂佺敤"
        )
    
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """鑾峰彇褰撳墠娲昏穬鐢ㄦ埛"""
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="鐢ㄦ埛宸茬鐢?")
    return current_user


def require_role(roles: list[str]):
    """瑙掕壊鏉冮檺瑁呴グ鍣?"""
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="鏉冮檺涓嶈冻"
            )
        return current_user
    return role_checker
