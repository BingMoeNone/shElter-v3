# shElter-v3

[![Version](https://img.shields.io/badge/version-3.1.0-blue)](https://github.com/shelter-v3)
[![Python](https://img.shields.io/badge/python-3.10+-green)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.109.0-blue)](https://fastapi.tiangolo.com/)
[![Vue](https://img.shields.io/badge/vue-3.x-green)](https://vuejs.org/)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

> 基于 FastAPI + Vue 3 的现代化 Wiki 平台，支持文章管理、用户社交、音乐播放、地铁地图等特色功能。

## ✨ 项目介绍

shElter-v3 是一个现代化的 Wiki 平台，采用前后端分离架构，集成了以下核心功能：
- 📑 **文章系统** - Markdown 支持、版本控制、权限管理
- 👥 **社交功能** - 用户关注、好友关系、个人主页
- 🎵 **音乐播放器** - 歌单管理、在线播放
- 🚇 **地铁地图** - 线路展示、站点查询
- 🔍 **搜索功能** - 全文搜索、分类浏览
- 🔐 **安全认证** - JWT RS256、Rate Limiting

## 🏗️ 项目架构

```
shElter-v3/
├── backend/              # FastAPI 后端
│   ├── src/
│   │   ├── api/         # API 路由
│   │   ├── auth/        # JWT 认证 (RS256)
│   │   ├── core/        # 核心模块
│   │   ├── models/      # 数据库模型
│   │   └── services/    # 业务逻辑
│   ├── keys/            # RSA 密钥
│   ├── alembic/         # 数据库迁移
│   └── tests/           # 测试
├── frontend/            # Vue 3 前端
│   ├── src/
│   │   ├── components/  # Vue 组件
│   │   ├── views/       # 页面视图
│   │   ├── stores/      # Pinia 状态管理
│   │   └── services/    # API 服务
│   └── ...
├── specs/               # 项目规范文档
├── docker-compose.yml   # Docker 编排
└── README.md
```

## 📊 版本对比

| 版本 | 评分 | 技术栈 | 特点 |
|------|------|--------|------|
| **v1** | 58/100 | PHP | 原始版本，功能完整但安全性差 |
| **v2** | 84/100 | FastAPI + Vue | 现代化重构，安全完善 |
| **v3** | 83/100 | FastAPI + Vue | Docker 优化，安全增强 |

**当前版本**: v3.1.0 (Security Enhanced)

## 🚀 快速开始

### 前置要求

| 组件 | 要求 |
|------|------|
| Python | 3.10+ |
| Node.js | 18+ |
| PostgreSQL | 15+ (可选 SQLite 开发) |
| Docker | 20+ (推荐) |

### Docker 部署 (推荐)

```bash
# 克隆项目
git clone https://github.com/your-repo/shelter-v3.git
cd shelter-v3

# 启动服务
docker-compose up -d

# 访问应用
# 前端：http://localhost:5173
# 后端：http://localhost:8000
# API 文档：http://localhost:8000/api/docs
```

### 手动部署

#### 1. 后端设置

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 .\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 生成 RSA 密钥
python generate_keys.py

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 启动服务
uvicorn src.main:app --reload
```

#### 2. 前端设置

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 📖 使用指南

### 用户功能

1. **注册/登录** - 访问 `/login` 或 `/register`
2. **创建文章** - 登录后点击"新建文章"
3. **编辑文章** - 文章页面点击"编辑"按钮
4. **社交互动** - 关注用户、发表评论

### API 使用

```bash
# 登录获取 Token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","username":"user","password":"Password123"}'

# 使用 Token 访问受保护资源
curl -X GET http://localhost:8000/api/v1/articles \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## ⚙️ 配置说明

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `DATABASE_URL` | SQLite | 数据库连接 |
| `ALGORITHM` | RS256 | JWT 加密算法 |
| `DEBUG` | False | 调试模式 |
| `RATE_LIMIT_ENABLED` | True | 启用频率限制 |

### 安全配置 (v3.1.0)

- JWT: RS256 非对称加密
- Rate Limiting: slowapi
- 密码：bcrypt 哈希
- 安全头：HSTS, X-Frame-Options 等

## 🧪 测试

```bash
# 后端测试
cd backend
pytest --cov=src

# 前端测试
cd frontend
npm run test
```

## 📚 项目文档

| 文档 | 说明 |
|------|------|
| [backend/README.md](backend/README.md) | 后端详细文档 |
| [UPGRADE_GUIDE.md](UPGRADE_GUIDE.md) | v3.1.0 升级指南 |
| [SECURITY_AUDIT_REPORT.md](SECURITY_AUDIT_REPORT.md) | 安全审计报告 |
| [specs/](specs/) | 项目规范文档 |

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 代码规范

- **Python**: PEP 8, 使用 `black` 格式化
- **前端**: Vue 3 + TypeScript, ESLint 检查
- **提交**: 使用清晰的提交信息格式
- **测试**: 新功能需包含对应测试

## ❓ 常见问题

### Q: 如何运行项目？
A: 推荐使用 Docker，详见上方"Docker 部署"部分。

### Q: 如何导入 v1 数据？
A: 
```bash
cd backend
python scripts/migrate_v1_users.py
python scripts/migrate_v1_content.py
python scripts/copy_music_files.py
```

### Q: 忘记密码怎么办？
A: 目前需通过数据库直接修改，后续版本会添加密码重置功能。

### Q: 如何成为管理员？
A: 运行 `python scripts/create_admin.py` 创建管理员账户。

### Q: v3.1.0 升级注意什么？
A: 请参考 [UPGRADE_GUIDE.md](UPGRADE_GUIDE.md) 进行升级。

## 📝 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-02-12 | 初始版本 |
| 3.0.0 | 2026-02-15 | v3 集成 |
| **3.1.0** | **2026-02-17** | **安全增强 (RS256, Rate Limiting)** |

## 📮 支持

- 提交 [Issue](https://github.com/your-repo/shelter-v3/issues)
- 加入讨论群
- 联系维护者

---

**shElter-v3** - 现代化 Wiki 平台
