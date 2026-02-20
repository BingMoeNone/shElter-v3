from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel
from fastapi import Request, status
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)


class ApiResponse(BaseModel):
    data: Any = None
    message: str = "鎿嶄綔鎴愬姛"
    status: int = 200
    timestamp: str = None
    error_code: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "data": {"id": 1, "name": "example"},
                "message": "鎿嶄綔鎴愬姛",
                "status": 200,
                "timestamp": "2026-02-17T10:00:00",
                "error_code": None
            }
        }


class ResponseWrapper:
    """缁熶竴鍝嶅簲鍖呰鍣?""

    @staticmethod
    def success(data: Any = None, message: str = "鎿嶄綔鎴愬姛", status_code: int = 200) -> dict:
        """鎴愬姛鍝嶅簲"""
        return {
            "data": data,
            "message": message,
            "status": status_code,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "error_code": None
        }

    @staticmethod
    def error(message: str, error_code: str = None, status_code: int = 400) -> dict:
        """閿欒鍝嶅簲"""
        return {
            "data": None,
            "message": message,
            "status": status_code,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "error_code": error_code
        }

    @staticmethod
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """鍏ㄥ眬寮傚父澶勭悊鍣?""
        logger.error(
            f"Unhandled exception: {str(exc)}",
            path=request.url.path,
            method=request.method
        )
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "data": None,
                "message": "鏈嶅姟鍣ㄥ唴閮ㄩ敊璇?,
                "status": 500,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "error_code": "INTERNAL_ERROR"
            }
        )

    @staticmethod
    async def validation_exception_handler(request: Request, exc) -> JSONResponse:
        """楠岃瘉寮傚父澶勭悊鍣?""
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "data": None,
                "message": "鏁版嵁楠岃瘉澶辫触",
                "status": 422,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "error_code": "VALIDATION_ERROR",
                "details": exc.errors() if hasattr(exc, 'errors') else str(exc)
            }
        )

    @staticmethod
    async def http_exception_handler(request: Request, exc) -> JSONResponse:
        """HTTP寮傚父澶勭悊鍣?""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "data": None,
                "message": exc.detail if hasattr(exc, 'detail') else str(exc),
                "status": exc.status_code,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "error_code": f"HTTP_{exc.status_code}"
            }
        )


response_wrapper = ResponseWrapper()
