from enum import Enum
from typing import Any, Optional
from fastapi import HTTPException, status


class ErrorCode(str, Enum):
    EMAIL_ALREADY_REGISTERED = "EMAIL_ALREADY_REGISTERED"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    USERNAME_EMAIL_MISMATCH = "USERNAME_EMAIL_MISMATCH"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    ACCOUNT_DEACTIVATED = "ACCOUNT_DEACTIVATED"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    ARTICLE_NOT_FOUND = "ARTICLE_NOT_FOUND"


class APIError(HTTPException):
    def __init__(
        self,
        code: ErrorCode,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[dict[str, Any]] = None,
        suggestion: Optional[str] = None,
    ):
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
    def __init__(self, email: str):
        super().__init__(
            code=ErrorCode.EMAIL_ALREADY_REGISTERED,
            message="璇ラ偖绠卞凡琚敞鍐?",
            status_code=status.HTTP_409_CONFLICT,
            details={"email": email},
            suggestion="璇蜂娇鐢ㄥ叾浠栭偖绠卞湴鍧€锛屾垨灏濊瘯鎵惧洖宸叉湁璐︽埛",
        )


class InvalidCredentialsError(APIError):
    def __init__(self):
        super().__init__(
            code=ErrorCode.INVALID_CREDENTIALS,
            message="鐢ㄦ埛鍚嶆垨瀵嗙爜閿欒",
            status_code=status.HTTP_401_UNAUTHORIZED,
            suggestion="璇锋鏌ユ偍鐨勭敤鎴峰悕鍜屽瘑鐮佹槸鍚︽纭?",
        )


class UsernameEmailMismatchError(APIError):
    def __init__(self, username: str, email: str):
        super().__init__(
            code=ErrorCode.USERNAME_EMAIL_MISMATCH,
            message="鐢ㄦ埛鍚嶄笌閭涓嶅尮閰?",
            status_code=status.HTTP_401_UNAUTHORIZED,
            details={"username": username, "email": email},
            suggestion="璇风‘璁ゆ偍杈撳叆鐨勭敤鎴峰悕涓庢敞鍐屾椂浣跨敤鐨勯偖绠辨槸鍚﹀尮閰?",
        )


class UserNotFoundError(APIError):
    def __init__(self, identifier: str):
        super().__init__(
            code=ErrorCode.USER_NOT_FOUND,
            message="鐢ㄦ埛涓嶅瓨鍦?",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"identifier": identifier},
            suggestion="璇锋鏌ョ敤鎴峰悕鎴栭偖绠辨槸鍚︽纭?",
        )


class AccountDeactivatedError(APIError):
    def __init__(self):
        super().__init__(
            code=ErrorCode.ACCOUNT_DEACTIVATED,
            message="璐︽埛宸茶鍋滅敤",
            status_code=status.HTTP_403_FORBIDDEN,
            suggestion="璇疯仈绯荤鐞嗗憳鎭㈠璐︽埛",
        )


class ArticleNotFoundError(APIError):
    def __init__(self, article_id: int):
        super().__init__(
            code=ErrorCode.ARTICLE_NOT_FOUND,
            message="鏂囩珷涓嶅瓨鍦?",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"article_id": article_id},
            suggestion="璇锋鏌ユ枃绔犳鍒╁瓨鍦ㄥ拰鏉冮檺",
        )
