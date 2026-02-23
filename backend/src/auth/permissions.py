﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from src.database import get_db
from src.models import User
from src.auth.jwt import get_current_user


# 瀹氫箟瑙掕壊灞傛缁撴瀯
ROLE_HIERARCHY = {
    "user": 1,
    "moderator": 2,
    "admin": 3
}

# 瀹氫箟鏉冮檺鏄犲皠
PERMISSIONS = {
    "user": [
        "read_articles",
        "create_articles",
        "update_own_articles",
        "delete_own_articles",
        "read_users",
        "update_own_profile",
        "create_comments",
        "update_own_comments",
        "delete_own_comments",
        "manage_connections"
    ],
    "moderator": [
        "read_articles",
        "create_articles",
        "update_own_articles",
        "delete_own_articles",
        "update_any_articles",
        "delete_any_articles",
        "read_users",
        "update_own_profile",
        "create_comments",
        "update_own_comments",
        "delete_own_comments",
        "delete_any_comments",
        "manage_connections",
        "moderate_content",
        "view_audit_logs"
    ],
    "admin": [
        "read_articles",
        "create_articles",
        "update_own_articles",
        "delete_own_articles",
        "update_any_articles",
        "delete_any_articles",
        "read_users",
        "update_users",
        "delete_users",
        "update_own_profile",
        "create_comments",
        "update_own_comments",
        "delete_own_comments",
        "delete_any_comments",
        "manage_connections",
        "moderate_content",
        "view_audit_logs",
        "manage_roles",
        "system_config"
    ]
}


def has_role(current_user: User, required_role: str) -> bool:
    """妫€鏌ョ敤鎴锋槸鍚﹀叿鏈夋寚瀹氳鑹叉垨鏇撮珮瑙掕壊"""
    user_role_level = ROLE_HIERARCHY.get(current_user.role, 0)
    required_role_level = ROLE_HIERARCHY.get(required_role, 0)
    return user_role_level >= required_role_level


def has_permission(current_user: User, permission: str) -> bool:
    """妫€鏌ョ敤鎴锋槸鍚﹀叿鏈夋寚瀹氭潈闄?""
    user_permissions = PERMISSIONS.get(current_user.role, [])
    return permission in user_permissions


def has_any_permission(current_user: User, permissions: List[str]) -> bool:
    """妫€鏌ョ敤鎴锋槸鍚﹀叿鏈変换鎰忔寚瀹氭潈闄?""
    user_permissions = PERMISSIONS.get(current_user.role, [])
    return any(perm in user_permissions for perm in permissions)


def has_all_permissions(current_user: User, permissions: List[str]) -> bool:
    """妫€鏌ョ敤鎴锋槸鍚﹀叿鏈夋墍鏈夋寚瀹氭潈闄?""
    user_permissions = PERMISSIONS.get(current_user.role, [])
    return all(perm in user_permissions for perm in permissions)


# 渚濊禆椤?- 瑙掕壊妫€鏌?async def require_role(required_role: str):
    """瑙掕壊妫€鏌ヤ緷璧栭」"""
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if not has_role(current_user, required_role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "FORBIDDEN", "message": f"闇€瑕亄required_role}鏉冮檺"}
            )
        return current_user
    return role_checker


# 渚濊禆椤?- 鏉冮檺妫€鏌?async def require_permission(permission: str):
    """鏉冮檺妫€鏌ヤ緷璧栭」"""
    async def permission_checker(current_user: User = Depends(get_current_user)) -> User:
        if not has_permission(current_user, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "FORBIDDEN", "message": f"缂哄皯{permission}鏉冮檺"}
            )
        return current_user
    return permission_checker


# 渚濊禆椤?- 浠绘剰鏉冮檺妫€鏌?async def require_any_permission(permissions: List[str]):
    """浠绘剰鏉冮檺妫€鏌ヤ緷璧栭」"""
    async def any_permission_checker(current_user: User = Depends(get_current_user)) -> User:
        if not has_any_permission(current_user, permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "FORBIDDEN", "message": f"缂哄皯鎵€闇€鏉冮檺"}
            )
        return current_user
    return any_permission_checker


# 渚濊禆椤?- 鎵€鏈夋潈闄愭鏌?async def require_all_permissions(permissions: List[str]):
    """鎵€鏈夋潈闄愭鏌ヤ緷璧栭」"""
    async def all_permission_checker(current_user: User = Depends(get_current_user)) -> User:
        if not has_all_permissions(current_user, permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "FORBIDDEN", "message": f"缂哄皯鎵€闇€鏉冮檺"}
            )
        return current_user
    return all_permission_checker


# 鏂囩珷鏉冮檺妫€鏌?def can_edit_article(current_user: User, article_author_id: str) -> bool:
    """妫€鏌ョ敤鎴锋槸鍚﹀彲浠ョ紪杈戞枃绔?""
    # 浣滆€呭彲浠ョ紪杈戣嚜宸辩殑鏂囩珷
    if str(current_user.id) == str(article_author_id):
        return True
    # 绠＄悊鍛樺拰鐗堜富鍙互缂栬緫鎵€鏈夋枃绔?    return has_role(current_user, "moderator")


def can_delete_article(current_user: User, article_author_id: str) -> bool:
    """妫€鏌ョ敤鎴锋槸鍚﹀彲浠ュ垹闄ゆ枃绔?""
    # 浣滆€呭彲浠ュ垹闄よ嚜宸辩殑鏂囩珷
    if str(current_user.id) == str(article_author_id):
        return True
    # 绠＄悊鍛樺拰鐗堜富鍙互鍒犻櫎鎵€鏈夋枃绔?    return has_role(current_user, "moderator")


# 璇勮鏉冮檺妫€鏌?def can_edit_comment(current_user: User, comment_author_id: str) -> bool:
    """妫€鏌ョ敤鎴锋槸鍚﹀彲浠ョ紪杈戣瘎璁?""
    # 浣滆€呭彲浠ョ紪杈戣嚜宸辩殑璇勮
    if str(current_user.id) == str(comment_author_id):
        return True
    # 绠＄悊鍛樺拰鐗堜富鍙互缂栬緫鎵€鏈夎瘎璁?    return has_role(current_user, "moderator")


def can_delete_comment(current_user: User, comment_author_id: str) -> bool:
    """妫€鏌ョ敤鎴锋槸鍚﹀彲浠ュ垹闄よ瘎璁?""
    # 浣滆€呭彲浠ュ垹闄よ嚜宸辩殑璇勮
    if str(current_user.id) == str(comment_author_id):
        return True
    # 绠＄悊鍛樺拰鐗堜富鍙互鍒犻櫎鎵€鏈夎瘎璁?    return has_role(current_user, "moderator")


# 鍐呭瀹℃牳鏉冮檺
def can_moderate_content(current_user: User) -> bool:
    """妫€鏌ョ敤鎴锋槸鍚﹀彲浠ュ鏍稿唴瀹?""
    return has_role(current_user, "moderator")


# 绯荤粺绠＄悊鏉冮檺
def can_manage_system(current_user: User) -> bool:
    """妫€鏌ョ敤鎴锋槸鍚﹀彲浠ョ鐞嗙郴缁?""
    return has_role(current_user, "admin")
