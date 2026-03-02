# -*- coding: utf-8 -*-
"""
错误定义模块

定义项目中使用的自定义错误类和错误码
"""
from enum import Enum
from typing import Any, Optional
from fastapi import HTTPException, status


class ErrorCode(str, Enum):
    """错误码枚举"""
    EMAIL_ALREADY_REGISTERED = "EMAIL_ALREADY_REGISTERED"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    USERNAME_EMAIL_MISMATCH = "USERNAME_EMAIL_MISMATCH"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    ACCOUNT_DEACTIVATED = "ACCOUNT_DEACTIVATED"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    ARTICLE_NOT_FOUND = "ARTICLE_NOT_FOUND"


class APIError(HTTPException):
    """
    API基础错误类
    
    所有自定义API错误的基类，继承自HTTPException
    """
    def __init__(
        self,
        code: ErrorCode,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[dict[str, Any]] = None,
        suggestion: Optional[str] = None,
    ):
        """
        初始化API错误
        
        Args:
            code: 错误码
            message: 错误消息
            status_code: HTTP状态码
            details: 错误详情
            suggestion: 错误建议
        """
        self.code = code
        self.message = message
        self.details = details or {}
        self.suggestion = suggestion
        
        detail = {
            "code": code.value,
            "message": message,
            "details": self.details,
        }
        if suggestion:
            detail["suggestion"] = suggestion
        
        super().__init__(status_code=status_code, detail=detail)


class EmailAlreadyRegisteredError(APIError):
    """
    邮箱已注册错误
    
    当用户尝试使用已注册的邮箱时抛出
    """
    def __init__(self, email: str):
        super().__init__(
            code=ErrorCode.EMAIL_ALREADY_REGISTERED,
            message="该邮箱已被注册",
            status_code=status.HTTP_409_CONFLICT,
            details={"email": email},
            suggestion="请使用其他邮箱地址，或尝试找回已有账户",
        )


class InvalidCredentialsError(APIError):
    """
    无效凭证错误
    
    当用户登录凭证无效时抛出
    """
    def __init__(self):
        super().__init__(
            code=ErrorCode.INVALID_CREDENTIALS,
            message="用户名或密码错误",
            status_code=status.HTTP_401_UNAUTHORIZED,
            suggestion="请检查您的用户名和密码是否正确",
        )


class UsernameEmailMismatchError(APIError):
    """
    用户名邮箱不匹配错误
    
    当用户名和邮箱不匹配时抛出
    """
    def __init__(self, username: str, email: str):
        super().__init__(
            code=ErrorCode.USERNAME_EMAIL_MISMATCH,
            message="用户名与邮箱不匹配",
            status_code=status.HTTP_401_UNAUTHORIZED,
            details={"username": username, "email": email},
            suggestion="请确认您输入的用户名与注册时使用的邮箱是否匹配",
        )


class UserNotFoundError(APIError):
    """
    用户不存在错误
    
    当查询的用户不存在时抛出
    """
    def __init__(self, identifier: str):
        super().__init__(
            code=ErrorCode.USER_NOT_FOUND,
            message="用户不存在",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"identifier": identifier},
            suggestion="请检查用户名或邮箱是否正确",
        )


class AccountDeactivatedError(APIError):
    """
    账户已停用错误
    
    当用户账户已被停用时抛出
    """
    def __init__(self):
        super().__init__(
            code=ErrorCode.ACCOUNT_DEACTIVATED,
            message="账户已被停用",
            status_code=status.HTTP_403_FORBIDDEN,
            suggestion="请联系管理员恢复账户",
        )


class ArticleNotFoundError(APIError):
    """
    文章不存在错误
    
    当查询的文章不存在时抛出
    """
    def __init__(self, article_id: int):
        super().__init__(
            code=ErrorCode.ARTICLE_NOT_FOUND,
            message="文章不存在",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"article_id": article_id},
            suggestion="请检查文章是否存在以及您是否有访问权限",
        )
