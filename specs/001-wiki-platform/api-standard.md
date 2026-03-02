# Wiki Platform API 接口规范与开发流程标准

## 1. 项目概述

### 1.1 项目背景
Wiki Platform是一个基于FastAPI后端和Vue3/HTML前端的内容管理系统，支持文章发布、用户管理、评论系统、内容审核等功能。

### 1.2 技术栈
- **后端**: FastAPI + SQLAlchemy + JWT认证
- **前端**: Vue 3 (TypeScript) / HTML/CSS/JavaScript
- **数据库**: SQLite/PostgreSQL
- **API规范**: OpenAPI 3.0.3

---

## 2. 现状分析

### 2.1 已识别的问题

#### 2.1.1 前后端接口调用不匹配问题

| 问题编号 | 问题类型 | 问题描述 | 影响范围 |
|---------|---------|---------|---------|
| P001 | 前端未调用真实API | 前端HTML文件使用mock函数进行模拟登录，没有调用后端真实API | login.html, index.html等 |
| P002 | 登录接口参数不匹配 | 后端使用email作为主要查询字段，前端mock使用username | 登录功能 |
| P003 | 后端代码存在乱码注释 | auth.py等文件存在乱码注释，影响代码可读性 | 后端API模块 |
| P004 | 类型转换错误 | jwt.py中refresh_token接口使用了int(user_id)转换，但User.id是字符串类型 | auth.py |
| P005 | CSS变量使用错误 | 前端多个文件使用了未定义的--color-background变量 | 前端HTML文件 |

#### 2.1.2 后端API接口清单（当前实现）

| 模块 | 路由前缀 | 接口方法 | 接口路径 | 状态 |
|------|---------|---------|---------|------|
| auth | /api/v1/auth | POST | /login | ✅ 已实现 |
| auth | /api/v1/auth | POST | /register | ✅ 已实现 |
| auth | /api/v1/auth | POST | /refresh | ✅ 已实现(需修复) |
| auth | /api/v1/auth | GET | /me | ✅ 已实现 |
| auth | /api/v1/auth | POST | /logout | ✅ 已实现 |
| users | /api/v1/users | GET | /me | ✅ 已实现 |
| users | /api/v1/users | GET | /{username} | ✅ 已实现 |
| users | /api/v1/users | PUT | /me | ✅ 已实现 |
| users | /api/v1/users | GET | /stats/{username} | ✅ 已实现 |
| articles | /api/v1/articles | GET | / | ✅ 已实现 |
| articles | /api/v1/articles | GET | /{article_id} | ✅ 已实现 |
| articles | /api/v1/articles | POST | / | ✅ 已实现 |
| articles | /api/v1/articles | PUT | /{article_id} | ✅ 已实现 |
| articles | /api/v1/articles | DELETE | /{article_id} | ✅ 已实现 |
| categories | /api/v1/categories | GET | / | ✅ 已实现 |
| categories | /api/v1/categories | GET | /{category_id} | ✅ 已实现 |
| categories | /api/v1/categories | POST | / | ✅ 已实现 |
| categories | /api/v1/categories | PUT | /{category_id} | ✅ 已实现 |
| tags | /api/v1/tags | GET | / | ✅ 已实现 |
| tags | /api/v1/tags | GET | /{tag_id} | ✅ 已实现 |
| tags | /api/v1/tags | POST | / | ✅ 已实现 |
| comments | /api/v1/comments | GET | / | ✅ 已实现 |
| comments | /api/v1/comments | POST | / | ✅ 已实现 |
| admin | /api/v1/admin | GET | /users | ✅ 已实现 |
| admin | /api/v1/admin | PUT | /users/{user_id} | ✅ 已实现 |
| moderation | /api/v1/moderation | GET | /articles | ✅ 已实现 |
| moderation | /api/v1/moderation | GET | /comments | ✅ 已实现 |
| music | /api/v1/music | GET | /tracks | ✅ 已实现 |
| metro | /api/v1/metro | GET | /stations | ✅ 已实现 |

---

## 3. 接口规范

### 3.1 认证接口

#### 3.1.1 用户登录
```
POST /api/v1/auth/login
```

**请求参数**:
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| username | string | 是 | 用户名 |
| email | string | 是 | 邮箱地址 |
| password | string | 是 | 密码 |

**响应格式**:
```json
{
  "success": true,
  "message": "登录成功",
  "data": {
    "access_token": "string",
    "refresh_token": "string",
    "token_type": "bearer",
    "user": {
      "id": "string",
      "username": "string",
      "email": "string",
      "role": "string",
      "is_active": boolean
    }
  }
}
```

#### 3.1.2 用户注册
```
POST /api/v1/auth/register
```

**请求参数**:
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| username | string | 是 | 用户名(3-30字符，只允许字母数字下划线) |
| email | string | 是 | 邮箱地址 |
| password | string | 是 | 密码(需包含大小写字母、数字、特殊字符，至少8位) |

#### 3.1.3 刷新令牌
```
POST /api/v1/auth/refresh
```

**请求参数**:
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| refresh_token | string | 是 | 刷新令牌 |

### 3.2 通用响应格式

#### 3.2.1 成功响应
```json
{
  "success": true,
  "message": "操作成功",
  "data": { ... }
}
```

#### 3.2.2 错误响应
```json
{
  "success": false,
  "message": "错误信息",
  "error_code": "ERROR_CODE",
  "status_code": 400
}
```

### 3.3 认证头要求
- 所有需要认证的接口必须在请求头中添加: `Authorization: Bearer <access_token>`
- Content-Type: `application/json`

---

## 4. 开发流程标准

### 4.1 接口开发流程

```
1. 需求分析
   └── 确定接口功能、参数、返回值

2. 接口设计
   └── 编写API规范（路径、方法、参数、响应）

3. 后端实现
   └── 创建/更新路由处理器、模型、schemas

4. 前端对接
   └── 实现API调用、错误处理、状态管理

5. 联调测试
   └── 验证接口调用正确性

6. 文档更新
   └── 更新API规范文档
```

### 4.2 接口命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 资源命名 | 使用复数形式 | /users, /articles |
| 路径参数 | 使用下划线命名 | /users/{user_id} |
| 查询参数 | 使用下划线命名 | ?page=1&limit=20 |
| 动作命名 | 使用HTTP方法 | POST创建, PUT更新 |

### 4.3 代码注释规范

#### 4.3.1 Python代码注释要求
- 所有文件头部添加编码声明: `# -*- coding: utf-8 -*-`
- 模块文件添加模块说明: `"""模块名称和功能描述"""`
- 函数添加文档字符串:
  ```python
  def function_name(param: type) -> return_type:
      """
      函数功能描述

      Args:
          param: 参数说明

      Returns:
          返回值说明
      """
  ```

#### 4.3.2 JavaScript代码注释要求
- 公共函数添加JSDoc注释
- 复杂逻辑添加行内注释

### 4.4 错误处理规范

| 错误类型 | HTTP状态码 | error_code |
|---------|-----------|-----------|
| 无效凭证 | 401 | INVALID_CREDENTIALS |
| 未授权访问 | 401 | UNAUTHORIZED |
| 权限不足 | 403 | FORBIDDEN |
| 资源不存在 | 404 | NOT_FOUND |
| 参数错误 | 400 | INVALID_PARAMS |
| 服务器错误 | 500 | INTERNAL_ERROR |

---

## 5. 修复计划

### 5.1 第一阶段：修复后端问题（P003, P004）

| 任务ID | 任务描述 | 优先级 | 状态 |
|--------|---------|--------|------|
| T001 | 修复auth.py乱码注释 | 高 | ✅ 已完成 |
| T002 | 修复jwt.py类型转换错误 | 高 | ✅ 已完成 |
| T003 | 检查并修复其他后端文件乱码 | 中 | 待处理 |

### 5.2 第二阶段：前端对接真实API（P001, P002）

| 任务ID | 任务描述 | 优先级 | 状态 |
|--------|---------|--------|------|
| T004 | 修改login.html调用真实API | 高 | 待处理 |
| T005 | 实现用户认证状态管理 | 高 | 待处理 |
| T006 | 修改其他页面调用真实API | 中 | 待处理 |

### 5.3 第三阶段：前端样式修复（P005）

| 任务ID | 任务描述 | 优先级 | 状态 |
|--------|---------|--------|------|
| T007 | 修复CSS变量问题 | 中 | ✅ 已完成(前端) |

---

## 6. 验证清单

### 6.1 后端验证
- [ ] auth.py 乱码注释已修复
- [ ] jwt.py 类型转换错误已修复
- [ ] 所有API接口可以正常响应
- [ ] 登录/注册功能正常工作

### 6.2 前端验证
- [ ] 前端可以调用后端真实API
- [ ] 登录状态可以正常保存和恢复
- [ ] 用户信息可以正常显示
- [ ] 所有页面CSS样式正常显示

### 6.3 集成验证
- [ ] 前后端接口完全匹配
- [ ] 错误处理机制正常工作
- [ ] API文档与实际实现一致

---

## 7. 附录

### 7.1 相关文件路径
- 后端入口: `backend/src/main.py`
- 后端配置: `backend/src/config.py`
- 认证模块: `backend/src/auth/jwt.py`
- API路由: `backend/src/api/`
- 前端工具: `frontend-legacy/utils.js`
- 前端页面: `frontend-legacy/*.html`

### 7.2 参考文档
- OpenAPI规范: `specs/001-wiki-platform/contracts/api.yaml`
- 数据模型: `specs/001-wiki-platform/data-model.md`

---

**文档版本**: 1.0.0
**创建日期**: 2026-02-25
**最后更新**: 2026-02-25
