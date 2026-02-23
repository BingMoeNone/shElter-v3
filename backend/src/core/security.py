from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from fastapi import Request
from typing import Callable


def get_real_ip(request: Request) -> str:
    """获取真实IP地址，考虑代理"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    return get_remote_address(request)


limiter = Limiter(key_func=get_real_ip)


def rate_limit(limit: str):
    """Rate Limiting装饰器"""
    return limiter.limit(limit)
