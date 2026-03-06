# shElter-v3 Backend

shElter-v3 后端服务基于 FastAPI 构建，采用了 Service-Oriented Monolith 架构，整合了 shElter-v2 的业务逻辑和 shElter-v1 的特色数据（Metro/Music）。

## 🛠 技术栈

- **框架**: FastAPI 0.109.0
- **数据库**: PostgreSQL + SQLAlchemy 2.0
- **迁移工具**: Alembic
- **验证**: Pydantic 2.0
- **认证**: JWT (RS256 非对称加密)
- **安全**: slowapi (Rate Limiting)

## 🎯 功能特性

### 核心功能
- 📝 **文章系统** - 创建、编辑、发布、版本控制
- 👤 **用户系统** - 注册、登录、RBAC 权限控制
- 📂 **分类管理** - 层级分类、标签体系
- 💬 **评论系统** - 嵌套评论、权限控制
- 🔍 **搜索功能** - 全文搜索、高级筛选
- 👥 **社交功能** - 用户关注、好友关系

### 特色模块
- 🎵 **音乐播放器** - 音乐列表、元数据管理
- 🚇 **地铁地图** - 线路数据、站点信息

### 安全特性 (v3.1.0)
- 🔐 JWT RS256 非对称加密
- ⚡ Rate Limiting 请求频率限制
- 🛡️ 统一响应格式
- 🔒 安全响应头 (HSTS, X-Frame-Options 等)
- 🔑 密码 bcrypt 哈希

## 🚀 快速开始

### 环境要求

| 组件 | 最低版本 |
|------|----------|
| Python | 3.10+ |
| PostgreSQL | 15+ |
| Node.js | 18+ (前端) |

### 1. 环境准备

```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 生成 RSA 密钥 (v3.1.0 安全升级)

```bash
# 自动生成 RSA 密钥对
python generate_keys.py
```

这将创建：
- `keys/private_key.pem` - 私钥 (务必保密!)
- `keys/public_key.pem` - 公钥

### 4. 数据库配置

创建 `.env` 文件（参考 `.env.example`）：

```env
# 数据库
DATABASE_URL=postgresql://user:password@localhost/shelter_v3

# JWT 配置 (v3.1.0 强制 RS256)
ALGORITHM=RS256
PRIVATE_KEY_PATH=keys/private_key.pem
PUBLIC_KEY_PATH=keys/public_key.pem
SECRET_KEY=your-secret-key-change-in-production

# Token 设置
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# 安全设置
DEBUG=False

# Rate Limiting
RATE_LIMIT_ENABLED=True
```

### 5. 数据库迁移

初始化数据库结构：

```bash
alembic upgrade head
```

### 6. 数据迁移 (从 v1)

如果你需要导入 shElter-v1 的数据，请按顺序执行以下脚本：

```bash
# 1. 迁移用户数据
python scripts/migrate_v1_users.py

# 2. 迁移文章与评论内容
python scripts/migrate_v1_content.py

# 3. 复制音乐文件
python scripts/copy_music_files.py
```

### 7. 启动服务

```bash
# 开发模式
uvicorn src.main:app --reload

# 生产模式
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

服务将在 `http://localhost:8000` 启动。

## 📖 API 文档

启动服务后，访问以下地址查看完整接口文档：

| 文档 | 地址 |
|------|------|
| Swagger UI | http://localhost:8000/api/docs |
| ReDoc | http://localhost:8000/api/redoc |
| OpenAPI JSON | http://localhost:8000/api/openapi.json |

### API 端点概览

| 模块 | 前缀 | 描述 |
|------|------|------|
| 认证 | `/api/v1/auth` | 登录、注册、刷新令牌 |
| 用户 | `/api/v1/users` | 用户资料、关注 |
| 文章 | `/api/v1/articles` | CRUD、版本控制 |
| 分类 | `/api/v1/categories` | 分类管理 |
| 标签 | `/api/v1/tags` | 标签管理 |
| 评论 | `/api/v1/comments` | 评论系统 |
| 搜索 | `/api/v1/search` | 全文搜索 |
| Metro | `/api/v1/metro` | 地铁数据 |
| Music | `/api/v1/music` | 音乐管理 |

## 🎵 静态资源

- **音乐文件**: 挂载于 `/static/music`，可通过 `/music/filename.mp3` 直接访问。
- **Metro API**: `/api/v1/metro` 提供地铁线路与站点数据。
- **Music API**: `/api/v1/music` 提供音乐列表与元数据。

## 🧪 测试

运行测试套件：

```bash
# 所有测试
pytest

# 带覆盖率
pytest --cov=src --cov-report=html

# 特定模块
pytest tests/test_auth.py -v
```

## ⚙️ 配置说明

### 环境变量

| 变量 | 默认值 | 描述 |
|------|--------|------|
| `DATABASE_URL` | - | PostgreSQL 连接字符串 |
| `ALGORITHM` | RS256 | JWT 加密算法 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 30 | Access Token 过期时间 |
| `REFRESH_TOKEN_EXPIRE_DAYS` | 7 | Refresh Token 过期时间 |
| `DEBUG` | False | 调试模式 |
| `RATE_LIMIT_ENABLED` | True | 启用 Rate Limiting |

### Rate Limiting 配置

| 端点 | 限制 |
|------|------|
| `/auth/login` | 10次/分钟 |
| `/auth/register` | 5次/分钟 |
| `/auth/refresh` | 10次/分钟 |
| 其他API | 60次/分钟 |

## 🐳 Docker 部署

### 使用 Docker Compose

```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f backend

# 停止
docker-compose down
```

### 构建镜像

```bash
docker build -t shelter-v3-backend:latest .
```

## 📁 项目结构

```
backend/
├── src/
│   ├── api/              # API 路由
│   │   ├── auth.py        # 认证接口
│   │   ├── articles.py    # 文章接口
│   │   ├── users.py       # 用户接口
│   │   └── ...
│   ├── auth/             # JWT 认证
│   │   └── jwt.py        # RS256 加密
│   ├── core/             # 核心模块
│   │   ├── response.py   # 统一响应
│   │   └── security.py   # Rate Limiter
│   ├── models/           # SQLAlchemy 模型
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # 业务逻辑
│   ├── utils/            # 工具函数
│   └── main.py           # 应用入口
├── keys/                 # RSA 密钥
├── alembic/              # 数据库迁移
├── scripts/              # 数据迁移脚本
├── tests/                # 测试
├── requirements.txt      # Python 依赖
├── generate_keys.py      # RSA 密钥生成
└── Dockerfile
```

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. **Fork** 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建 **Pull Request**

### 代码规范

- Python: 遵循 PEP 8，使用 `black` 和 `isort` 格式化
- 提交信息: 使用清晰的提交信息格式
- 测试: 新增功能需包含相应测试

## ❓ 常见问题

### Q: 如何重置密码？
A: 当前版本通过数据库直接修改用户密码，或等后续版本实现密码重置功能。

### Q: 如何添加管理员用户？
A: 运行 `python scripts/create_admin.py` 创建管理员账户。

### Q: 如何备份数据？
A: 使用 PostgreSQL 的 `pg_dump` 命令进行数据库备份：

```bash
pg_dump -U user shelter_v3 > backup.sql
```

### Q: v3.1.0 升级后需要做什么？
A: 请参考 [UPGRADE_GUIDE.md](../UPGRADE_GUIDE.md) 进行升级。

## 📜 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-02-12 | 初始版本 |
| 3.0.0 | 2026-02-15 | v3 集成 |
| **3.1.0** | **2026-02-17** | **安全增强 (RS256, Rate Limiting)** |

## 📞 支持

如有问题，请提交 Issue 或联系维护者。

---

**shElter-v3** - 基于 FastAPI 的现代化 Wiki 平台
