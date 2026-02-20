from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional

from src.database import get_db
from src.models import User, AuditLog
from src.schemas import UserResponse, Pagination
from src.schemas.admin import AdminUserResponse, AdminUserUpdate, AdminPasswordReset, AuditLogResponse
from src.auth.jwt import get_current_user, get_password_hash, verify_password, require_role
from src.services.audit import audit_service
from src.utils.errors import APIError, ErrorCode

router = APIRouter()


# 浣跨敤鏂扮殑鏉冮檺绯荤粺
def require_admin():
    return require_role(["admin"])


@router.get("/users", response_model=dict)
async def admin_list_users(
    page: int = 1,
    limit: int = 20,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin()),
    request: Request = None,
):
    query = db.query(User)
    
    if search:
        query = query.filter(
            User.username.ilike(f"%{search}%") | 
            User.email.ilike(f"%{search}%") |
            User.display_name.ilike(f"%{search}%")
        )
    
    total = query.count()
    users = query.offset((page - 1) * limit).limit(limit).all()
    
    audit_service.log(
        db=db,
        operator_id=str(admin.id),
        operator_username=admin.username,
        action="USER_LIST",
        target_type="system",
        details={"page": page, "limit": limit, "search": search},
        request=request,
    )
    
    return {
        "users": [AdminUserResponse.model_validate(u) for u in users],
        "pagination": Pagination(
            page=page,
            limit=limit,
            total_pages=(total + limit - 1) // limit,
            total_items=total
        ).model_dump()
    }


@router.get("/users/{user_id}", response_model=AdminUserResponse)
async def admin_get_user(
    user_id: str,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin()),
    request: Request = None,
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="鐢ㄦ埛涓嶅瓨鍦?)
    
    audit_service.log(
        db=db,
        operator_id=str(admin.id),
        operator_username=admin.username,
        action="USER_VIEW",
        target_type="user",
        target_id=user_id,
        target_info={"username": user.username, "email": user.email},
        request=request,
    )
    
    return AdminUserResponse.model_validate(user)


@router.put("/users/{user_id}", response_model=AdminUserResponse)
async def admin_update_user(
    user_id: str,
    user_data: AdminUserUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin()),
    request: Request = None,
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="鐢ㄦ埛涓嶅瓨鍦?)
    
    old_data = {
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
    }
    
    update_data = user_data.model_dump(exclude_unset=True)
    changes = {}
    
    for key, value in update_data.items():
        if key == "username" and value != user.username:
            changes["username"] = {"old": user.username, "new": value}
            audit_service.log(
                db=db,
                operator_id=str(admin.id),
                operator_username=admin.username,
                action="USER_USERNAME_CHANGE",
                target_type="user",
                target_id=user_id,
                target_info={"username": user.username},
                details={"old_username": user.username, "new_username": value},
                request=request,
            )
        elif key == "email" and value != user.email:
            existing = db.query(User).filter(User.email == value).first()
            if existing:
                raise HTTPException(status_code=409, detail="閭宸茶浣跨敤")
            changes["email"] = {"old": user.email, "new": value}
            audit_service.log(
                db=db,
                operator_id=str(admin.id),
                operator_username=admin.username,
                action="USER_EMAIL_CHANGE",
                target_type="user",
                target_id=user_id,
                target_info={"email": user.email},
                details={"old_email": user.email, "new_email": value},
                request=request,
            )
        elif key == "role" and value != user.role:
            changes["role"] = {"old": user.role, "new": value}
            audit_service.log(
                db=db,
                operator_id=str(admin.id),
                operator_username=admin.username,
                action="USER_ROLE_CHANGE",
                target_type="user",
                target_id=user_id,
                target_info={"username": user.username},
                details={"old_role": user.role, "new_role": value},
                request=request,
            )
        
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    
    audit_service.log(
        db=db,
        operator_id=str(admin.id),
        operator_username=admin.username,
        action="USER_UPDATE",
        target_type="user",
        target_id=user_id,
        target_info={"username": user.username, "email": user.email},
        details={"changes": changes},
        request=request,
    )
    
    return AdminUserResponse.model_validate(user)


@router.post("/users/{user_id}/reset-password")
async def admin_reset_password(
    user_id: str,
    password_data: AdminPasswordReset,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin()),
    request: Request = None,
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="鐢ㄦ埛涓嶅瓨鍦?)
    
    user.password_hash = get_password_hash(password_data.new_password)
    db.commit()
    
    audit_service.log(
        db=db,
        operator_id=str(admin.id),
        operator_username=admin.username,
        action="USER_PASSWORD_RESET",
        target_type="user",
        target_id=user_id,
        target_info={"username": user.username, "email": user.email},
        request=request,
    )
    
    return {"message": "瀵嗙爜宸查噸缃?}


@router.delete("/users/{user_id}")
async def admin_delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin()),
    request: Request = None,
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="鐢ㄦ埛涓嶅瓨鍦?)
    
    if str(user.id) == str(admin.id):
        raise HTTPException(status_code=400, detail="涓嶈兘鍒犻櫎鑷繁鐨勮处鎴?)
    
    user_info = {"username": user.username, "email": user.email}
    
    db.delete(user)
    db.commit()
    
    audit_service.log(
        db=db,
        operator_id=str(admin.id),
        operator_username=admin.username,
        action="USER_DELETE",
        target_type="user",
        target_id=user_id,
        target_info=user_info,
        request=request,
    )
    
    return {"message": "鐢ㄦ埛宸插垹闄?}


@router.get("/logs", response_model=dict)
async def admin_get_logs(
    page: int = 1,
    limit: int = 50,
    user_id: Optional[str] = None,
    action: Optional[str] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin()),
):
    query = db.query(AuditLog)
    
    if user_id:
        query = query.filter(AuditLog.target_id == user_id)
    if action:
        query = query.filter(AuditLog.action == action)
    
    total = query.count()
    logs = query.order_by(AuditLog.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    
    return {
        "logs": [AuditLogResponse.model_validate(log) for log in logs],
        "pagination": Pagination(
            page=page,
            limit=limit,
            total_pages=(total + limit - 1) // limit,
            total_items=total
        ).model_dump()
    }
