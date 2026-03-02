# API 调用规范与错误处理指南

## 📋 目录

1. [概述](#概述)
2. [API 接口清单](#api-接口清单)
3. [标准调用方式](#标准调用方式)
4. [错误处理](#错误处理)
5. [最佳实践](#最佳实践)
6. [使用示例](#使用示例)

## 概述

本文档定义了前端与后端 API 调用的标准规范，确保前后端接口一致性和错误处理的统一性。

### 核心原则

- ✅ **统一性**: 所有 API 调用使用统一的 `callAPI` 函数
- ✅ **安全性**: 自动处理认证令牌和错误状态
- ✅ **可靠性**: 内置重试机制和超时控制
- ✅ **可维护性**: 清晰的错误处理和日志记录
- ✅ **性能优化**: 支持缓存和速率限制

## API 接口清单

### 认证相关 API (`/api/v1/auth`)

| 接口 | 方法 | 路径 | 认证 | 速率限制 | 描述 |
|------|------|------|------|----------|------|
| 登录 | POST | `/auth/login` | ❌ | 10/分钟 | 用户登录 |
| 注册 | POST | `/auth/register` | ❌ | 5/分钟 | 用户注册 |

### 文章相关 API (`/api/v1/articles`)

| 接口 | 方法 | 路径 | 认证 | 描述 |
|------|------|------|------|------|
| 获取文章列表 | GET | `/articles` | ❌ | 获取文章列表（支持分页、排序、过滤） |
| 获取文章详情 | GET | `/articles/{id}` | ❌ | 获取单篇文章详情 |
| 创建文章 | POST | `/articles` | ✅ | 创建新文章 |
| 更新文章 | PUT | `/articles/{id}` | ✅ | 更新文章（仅作者） |

### 参数说明

#### 获取文章列表参数

```javascript
{
    title: 'string (可选，模糊搜索)',
    category_id: 'number (可选)',
    tag_id: 'number (可选)',
    author_id: 'number (可选)',
    skip: 'number (可选，默认 0)',
    limit: 'number (可选，默认 10，最大 100)',
    sort_by: 'string (可选，默认 created_at)',
    sort_order: 'string (可选，默认 desc)'
}
```

## 标准调用方式

### 基本用法

```javascript
// 引入必要的文件
<script src="config.js"></script>
<script src="utils.js"></script>
<script src="api-client.js"></script>

// 调用 API
async function loadData() {
    try {
        const result = await callAPI('GET', '/articles', {
            params: {
                limit: 20,
                sort_by: 'created_at'
            },
            requiresAuth: false
        });
        
        console.log('数据:', result.data);
    } catch (error) {
        const errorInfo = handleAPIError(error);
        console.error('错误:', errorInfo);
    }
}
```

### callAPI 函数参数

```javascript
/**
 * @param {string} method - HTTP 方法 (GET, POST, PUT, DELETE)
 * @param {string} url - API 路径 (不包含 BASE_URL)
 * @param {Object} options - 配置选项
 * @param {Object} options.params - URL 查询参数
 * @param {Object} options.body - 请求体
 * @param {boolean} options.requiresAuth - 是否需要认证
 * @param {number} options.timeout - 超时时间（毫秒）
 * @param {number} options.retryCount - 重试次数
 */
```

## 错误处理

### 错误类型

#### 1. APIError (API 返回的错误)

```javascript
class APIError extends Error {
    status: number;      // HTTP 状态码
    message: string;     // 错误消息
    errorCode: string;   // 错误代码
}
```

#### 2. 网络错误

```javascript
{
    status: 0,
    message: '网络错误',
    errorCode: 'NETWORK_ERROR'
}
```

#### 3. 超时错误

```javascript
{
    status: 0,
    message: '请求超时',
    errorCode: 'TIMEOUT'
}
```

### 错误处理函数

```javascript
function handleAPIError(error) {
    // 返回统一的错误信息格式
    return {
        status: error.status,
        message: error.message,
        errorCode: error.errorCode,
        suggestion: '错误处理建议'
    };
}
```

### 常见错误代码

| 状态码 | 错误代码 | 说明 | 处理建议 |
|--------|----------|------|----------|
| 400 | BAD_REQUEST | 请求参数错误 | 检查输入参数 |
| 401 | UNAUTHORIZED | 未认证 | 跳转到登录页 |
| 403 | FORBIDDEN | 无权限 | 提示用户无权限 |
| 404 | NOT_FOUND | 资源不存在 | 提示资源不存在 |
| 429 | RATE_LIMIT_EXCEEDED | 请求过于频繁 | 稍后重试 |
| 500 | INTERNAL_ERROR | 服务器错误 | 稍后重试 |
| 503 | SERVICE_UNAVAILABLE | 服务不可用 | 稍后重试 |

## 最佳实践

### 1. 始终使用 callAPI 函数

```javascript
// ✅ 好的做法
const result = await callAPI('GET', '/articles', { requiresAuth: false });

// ❌ 不好的做法
const result = await fetch('/articles');
```

### 2. 正确处理错误

```javascript
// ✅ 好的做法
try {
    const result = await callAPI('POST', '/articles', {
        body: data,
        requiresAuth: true
    });
} catch (error) {
    const errorInfo = handleAPIError(error);
    notificationManager.error(errorInfo.message);
}

// ❌ 不好的做法
try {
    const result = await callAPI('POST', '/articles', {
        body: data,
        requiresAuth: true
    });
} catch (error) {
    console.error(error); // 没有给用户提示
}
```

### 3. 使用通知管理器

```javascript
// ✅ 好的做法
try {
    await createArticle(data);
    notificationManager.success('创建成功！');
} catch (error) {
    notificationManager.error(error.message);
}

// ❌ 不好的做法
try {
    await createArticle(data);
    alert('创建成功！');
} catch (error) {
    alert('创建失败！');
}
```

### 4. 添加加载状态

```javascript
// ✅ 好的做法
async function loadArticles() {
    showLoading();
    try {
        const articles = await getArticles();
        renderArticles(articles);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

// ❌ 不好的做法
async function loadArticles() {
    const articles = await getArticles(); // 没有加载状态
    renderArticles(articles);
}
```

### 5. 使用缓存优化性能

```javascript
// ✅ 好的做法（带缓存）
async function getArticlesWithCache(params, forceRefresh = false) {
    const cacheKey = 'articles_' + JSON.stringify(params);
    
    if (!forceRefresh && CONFIG.CACHE.ENABLE_CACHE) {
        const cached = localStorage.getItem(cacheKey);
        if (cached) {
            const { data, timestamp } = JSON.parse(cached);
            if (Date.now() - timestamp < CONFIG.CACHE.ARTICLES_TTL) {
                return data;
            }
        }
    }
    
    const result = await getArticles(params);
    
    if (CONFIG.CACHE.ENABLE_CACHE) {
        localStorage.setItem(cacheKey, JSON.stringify({
            data: result,
            timestamp: Date.now()
        }));
    }
    
    return result;
}
```

## 使用示例

### 示例 1: 用户登录

```javascript
async function handleLogin(username, email, password) {
    const loginButton = document.getElementById('loginButton');
    const errorMessage = document.getElementById('errorMessage');
    
    // 禁用按钮，显示加载状态
    loginButton.disabled = true;
    loginButton.textContent = '登录中...';
    errorMessage.style.display = 'none';
    
    try {
        const result = await callAPI('POST', '/auth/login', {
            body: { username, email, password },
            requiresAuth: false
        });
        
        // 保存认证信息
        const token = result.data.access_token;
        const user = result.data.user;
        const expiry = Date.now() + (30 * 60 * 1000);
        authManager.saveAuth(token, user, expiry);
        
        // 显示成功消息
        notificationManager.success('登录成功！');
        
        // 跳转到首页
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 1000);
        
    } catch (error) {
        const errorInfo = handleAPIError(error);
        
        // 显示错误消息
        errorMessage.textContent = errorInfo.message;
        errorMessage.style.display = 'block';
        
        // 重置按钮状态
        loginButton.disabled = false;
        loginButton.textContent = '登录';
    }
}
```

### 示例 2: 获取文章列表

```javascript
async function loadArticles(page = 1, pageSize = 10) {
    const loadingElement = document.getElementById('loading');
    const articlesListElement = document.getElementById('articles-list');
    
    // 显示加载状态
    loadingElement.style.display = 'flex';
    articlesListElement.style.display = 'none';
    
    try {
        const result = await callAPI('GET', '/articles', {
            params: {
                skip: (page - 1) * pageSize,
                limit: pageSize,
                sort_by: 'created_at',
                sort_order: 'desc'
            },
            requiresAuth: false
        });
        
        // 渲染文章列表
        renderArticles(result.data.items);
        
        // 更新分页
        updatePagination(page, result.data.total, pageSize);
        
        // 显示列表
        loadingElement.style.display = 'none';
        articlesListElement.style.display = 'flex';
        
    } catch (error) {
        const errorInfo = handleAPIError(error);
        
        // 显示错误状态
        loadingElement.style.display = 'none';
        showError('加载文章失败：' + errorInfo.message);
    }
}
```

### 示例 3: 创建文章

```javascript
async function handleCreateArticle(articleData) {
    const submitButton = document.getElementById('submit');
    
    // 禁用按钮
    submitButton.disabled = true;
    submitButton.textContent = '创建中...';
    
    try {
        // 验证数据
        if (!articleData.title || !articleData.content) {
            throw new Error('标题和内容不能为空');
        }
        
        const result = await callAPI('POST', '/articles', {
            body: {
                title: articleData.title,
                content: articleData.content,
                category_id: articleData.categoryId,
                tags: articleData.tags || []
            },
            requiresAuth: true
        });
        
        // 显示成功消息
        notificationManager.success('文章创建成功！');
        
        // 跳转到文章详情页
        setTimeout(() => {
            window.location.href = `article-detail.html?id=${result.data.id}`;
        }, 1000);
        
    } catch (error) {
        const errorInfo = handleAPIError(error);
        
        // 显示错误消息
        notificationManager.error(errorInfo.message);
        
        // 重置按钮状态
        submitButton.disabled = false;
        submitButton.textContent = '创建';
    }
}
```

## 配置文件说明

### config.js 配置项

```javascript
CONFIG = {
    API: {
        BASE_URL: 'http://127.0.0.1:8000/api/v1',  // API 基础 URL
        TIMEOUT: 10000,                             // 超时时间（毫秒）
        RETRY_COUNT: 3,                             // 重试次数
        RETRY_DELAY: 1000,                          // 重试延迟（毫秒）
        RATE_LIMIT: {                               // 速率限制配置
            LOGIN: '10/minute',
            REGISTER: '5/minute',
            COMMENT: '20/minute',
            DEFAULT: '100/minute'
        }
    },
    
    ERROR_HANDLING: {
        RETRY_STATUS_CODES: [408, 429, 500, 502, 503, 504],  // 自动重试的状态码
        AUTH_ERROR_CODES: [401, 403],                        // 需要重新认证的状态码
        ERROR_MESSAGE_DURATION: 5000,                        // 错误提示显示时间
        SUCCESS_MESSAGE_DURATION: 3000                       // 成功提示显示时间
    },
    
    CACHE: {
        ENABLE_CACHE: true,           // 是否启用缓存
        DEFAULT_TTL: 5 * 60 * 1000,   // 默认缓存时间（5 分钟）
        ARTICLES_TTL: 10 * 60 * 1000, // 文章列表缓存时间
        USER_TTL: 30 * 60 * 1000      // 用户信息缓存时间
    }
}
```

## 相关文件

- `config.js` - 配置文件
- `api-client.js` - API 客户端核心函数
- `api-examples.js` - 使用示例
- `utils.js` - 工具函数（包含 AuthManager、NotificationManager 等）

## 更新日志

### v1.1.0 (2026-02-28)
- ✅ 添加标准化的 API 调用函数
- ✅ 完善错误处理机制
- ✅ 添加缓存支持
- ✅ 添加速率限制配置
- ✅ 创建完整的使用示例

---

**文档更新时间**: 2026-02-28  
**文档版本**: 1.1.0
