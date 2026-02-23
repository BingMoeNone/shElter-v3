import json
from datetime import datetime
from typing import Optional, Any

from sqlalchemy.orm import Session
from fastapi import Request

from src.models import AuditLog


class AuditService:
    ACTIONS = {
        "USER_CREATE": "创建用户",
        "USER_DELETE": "删除用户",
        "USER_UPDATE": "更新用户",
        "USER_PASSWORD_RESET": "重置密码",
        "USER_PASSWORD_CHANGE": "修改密码",
        "USER_USERNAME_CHANGE": "修改用户名",
        "USER_EMAIL_CHANGE": "修改邮箱",
        "USER_ROLE_CHANGE": "修改角色",
        "USER_VIEW": "查看用户",
        "USER_LIST": "列出用户",
        "ADMIN_LOGIN": "管理员登录",
    }

    @staticmethod
    def log(
        db: Session,
        operator_id: str,
        operator_username: str,
        action: str,
        target_type: str,
        target_id: Optional[str] = None,
        target_info: Optional[dict] = None,
        details: Optional[dict] = None,
        request: Optional[Request] = None,
        status: str = "success",
        error_message: Optional[str] = None,
    ) -> AuditLog:
        log_entry = AuditLog(
            operator_id=operator_id,
            operator_username=operator_username,
            action=action,
            target_type=target_type,
            target_id=target_id,
            target_info=json.dumps(target_info, ensure_ascii=False) if target_info else None,
            details=json.dumps(details, ensure_ascii=False) if details else None,
            ip_address=request.client.host if request and request.client else None,
            user_agent=request.headers.get("user-agent", "")[:500] if request else None,
            status=status,
            error_message=error_message,
        )
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        return log_entry

    @staticmethod
    def get_user_logs(db: Session, user_id: str, limit: int = 100):
        return db.query(AuditLog).filter(
            AuditLog.target_id == user_id
        ).order_by(AuditLog.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_operator_logs(db: Session, operator_id: str, limit: int = 100):
        return db.query(AuditLog).filter(
            AuditLog.operator_id == operator_id
        ).order_by(AuditLog.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_all_logs(db: Session, page: int = 1, limit: int = 50):
        total = db.query(AuditLog).count()
        logs = db.query(AuditLog).order_by(
            AuditLog.created_at.desc()
        ).offset((page - 1) * limit).limit(limit).all()
        return {"logs": logs, "total": total, "page": page, "limit": limit}


audit_service = AuditService()
