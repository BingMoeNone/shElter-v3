# 项目需求文档

## 项目名称
**数字避难所 | shElter**

---

## 核心功能

1. 给用户提供类wiki的共同创作、交友环境。

---

## 功能模块

### 1. 用户系统
- 用户注册与登录
- 个人资料管理
- 用户权限管理

### 2. 内容管理
- 文章创建与编辑
- 文章分类与标签
- 文章搜索与筛选

### 3. 社交功能
- 用户关注与粉丝
- 评论与互动
- 内容审核

### 4. 媒体管理
- 图片上传与管理
- 音乐文件管理
- 文件存储与分发

---

## 技术栈

### 后端
- Python 3.11+
- FastAPI
- SQLAlchemy
- SQLite/PostgreSQL

### 前端
- HTML5/CSS3/JavaScript
- 响应式设计
- RESTful API 集成

---

## 项目结构

```
shElter-v3/
├── backend/          # 后端服务
├── frontend-legacy/  # 前端页面
├── docs/             # 文档
├── specs/            # 规范与计划
└── README.md         # 项目说明
```

---

## 开发规范

1. 遵循 RESTful API 设计规范
2. 使用 Git 进行版本控制
3. 编写单元测试
4. 代码审查与文档更新

---

## 部署说明

### 后端启动
```bash
cd backend
python -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
```

### 前端启动
```bash
cd frontend-legacy
python -m http.server 8080
```

---

*文档版本: v1.0*  
*最后更新: 2026-03-05*
