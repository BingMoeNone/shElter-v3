from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from uuid import uuid4

from src.database import get_db
from src.auth.jwt import get_current_user
from src.models import User

router = APIRouter()

# 文件存储目录
MEDIA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static", "media")

# 确保目录存在
os.makedirs(MEDIA_DIR, exist_ok=True)

# 允许的文件类型
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
ALLOWED_FILE_TYPES = ALLOWED_IMAGE_TYPES.union({"application/pdf", "text/plain"})

# 最大文件大小 (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """上传媒体文件"""
    # 检查文件大小
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "文件大小不能超过10MB", "error_code": "FILE_TOO_LARGE"}
        )
    
    # 检查文件类型
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "不支持的文件类型", "error_code": "INVALID_FILE_TYPE"}
        )
    
    # 生成唯一文件名
    file_extension = os.path.splitext(file.filename)[1] if "." in file.filename else ""
    unique_filename = f"{uuid4()}{file_extension}"
    
    # 构建文件路径
    file_path = os.path.join(MEDIA_DIR, unique_filename)
    
    # 保存文件
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "文件保存失败", "error_code": "FILE_SAVE_ERROR"}
        )
    
    # 返回文件URL
    file_url = f"/static/media/{unique_filename}"
    
    return {
        "url": file_url,
        "filename": unique_filename,
        "original_filename": file.filename,
        "content_type": file.content_type,
        "size": file.size
    }


@router.post("/upload-multiple", status_code=status.HTTP_201_CREATED)
async def upload_multiple_files(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """批量上传媒体文件"""
    results = []
    
    for file in files:
        # 检查文件大小
        if file.size > MAX_FILE_SIZE:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": "文件大小不能超过10MB"
            })
            continue
        
        # 检查文件类型
        if file.content_type not in ALLOWED_FILE_TYPES:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": "不支持的文件类型"
            })
            continue
        
        # 生成唯一文件名
        file_extension = os.path.splitext(file.filename)[1] if "." in file.filename else ""
        unique_filename = f"{uuid4()}{file_extension}"
        
        # 构建文件路径
        file_path = os.path.join(MEDIA_DIR, unique_filename)
        
        # 保存文件
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # 构建文件URL
            file_url = f"/static/media/{unique_filename}"
            
            results.append({
                "filename": file.filename,
                "success": True,
                "url": file_url,
                "unique_filename": unique_filename,
                "content_type": file.content_type,
                "size": file.size
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": "文件保存失败"
            })
    
    return {
        "results": results,
        "total": len(files),
        "success_count": sum(1 for r in results if r["success"])
    }
