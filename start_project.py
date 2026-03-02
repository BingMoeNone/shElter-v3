# -*- coding: utf-8 -*-
"""
Wiki Platform V3 启动器
"""
import subprocess
import sys
import os

def start_backend():
    """启动后端服务"""
    print("正在启动后端服务...")
    os.chdir(r"c:\BM_Program\shElter-v3\backend")
    subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "src.main:app", 
        "--host", "127.0.0.1", 
        "--port", "8000"
    ])
    print("后端服务已启动: http://127.0.0.1:8000")

def start_frontend():
    """启动前端服务"""
    print("正在启动前端服务...")
    os.chdir(r"c:\BM_Program\shElter-v3\frontend-legacy")
    subprocess.Popen([
        sys.executable, "-m", "http.server", "8080"
    ])
    print("前端服务已启动: http://localhost:8080")

if __name__ == "__main__":
    print("=" * 50)
    print("Wiki Platform V3 启动器")
    print("=" * 50)
    
    # 启动后端
    start_backend()
    
    # 启动前端
    start_frontend()
    
    print("=" * 50)
    print("所有服务已启动！")
    print("前端: http://localhost:8080")
    print("后端API: http://127.0.0.1:8000")
    print("API文档: http://127.0.0.1:8000/api/docs")
    print("=" * 50)
