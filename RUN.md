# Wiki Platform V3 启动脚本

## 后端启动方式

### 方式1：使用Python直接运行
```bash
cd c:\BM_Program\shElter-v3\backend
python -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
```

### 方式2：使用虚拟环境
```bash
cd c:\BM_Program\shElter-v3\backend
.venv\Scripts\python -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
```

## 前端启动方式

### 方式1：使用Python HTTP服务器（推荐）
```bash
cd c:\BM_Program\shElter-v3\frontend-legacy
python -m http.server 8080
```
然后访问: http://localhost:8080

### 方式2：使用Node.js http-server
```bash
cd c:\BM_Program\shElter-v3\frontend-legacy
npx http-server -p 8080
```

## API地址配置

前端HTML文件已配置为连接:
- 后端API: http://127.0.0.1:8000/api/v1

确保后端运行在端口8000，前端运行在端口8080。

## 访问地址

- 前端首页: http://localhost:8080/index.html
- 登录页面: http://localhost:8080/login.html
- 注册页面: http://localhost:8080/register.html
- API文档: http://127.0.0.1:8000/api/docs
