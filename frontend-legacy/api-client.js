/**
 * API 调用规范与错误处理指南
 * 
 * 本文档定义了前端与后端 API 调用的标准规范，确保前后端接口一致性和错误处理的统一性。
 */

// ============================================================================
// 1. API 接口清单
// ============================================================================

/**
 * 认证相关 API
 * 路由前缀：/api/v1/auth
 */
const AUTH_APIS = {
    // 用户登录
    LOGIN: {
        method: 'POST',
        url: '/auth/login',
        requiresAuth: false,
        rateLimit: '10/minute',
        body: {
            username: 'string (可选)',
            email: 'string (必填)',
            password: 'string (必填)'
        },
        response: {
            access_token: 'string',
            refresh_token: 'string',
            token_type: 'bearer',
            user: {
                id: 'number',
                username: 'string',
                email: 'string',
                role: 'string',
                is_active: 'boolean'
            }
        }
    },
    
    // 用户注册
    REGISTER: {
        method: 'POST',
        url: '/auth/register',
        requiresAuth: false,
        rateLimit: '5/minute',
        body: {
            email: 'string (必填)',
            username: 'string (必填)',
            password: 'string (必填，必须包含大小写字母、数字和特殊字符)'
        }
    }
};

/**
 * 文章相关 API
 * 路由前缀：/api/v1/articles
 */
const ARTICLE_APIS = {
    // 获取文章列表
    GET_ARTICLES: {
        method: 'GET',
        url: '/articles',
        requiresAuth: false,
        params: {
            title: 'string (可选，模糊搜索)',
            category_id: 'number (可选)',
            tag_id: 'number (可选)',
            author_id: 'number (可选)',
            skip: 'number (可选，默认 0)',
            limit: 'number (可选，默认 10，最大 100)',
            sort_by: 'string (可选，默认 created_at)',
            sort_order: 'string (可选，默认 desc)'
        }
    },
    
    // 获取文章详情
    GET_ARTICLE: {
        method: 'GET',
        url: '/articles/{article_id}',
        requiresAuth: false,
        params: {
            article_id: 'number (必填，路径参数)'
        }
    },
    
    // 创建文章
    CREATE_ARTICLE: {
        method: 'POST',
        url: '/articles',
        requiresAuth: true,
        body: {
            title: 'string (必填)',
            content: 'string (必填)',
            category_id: 'number (必填)',
            tags: 'array (可选)'
        }
    },
    
    // 更新文章
    UPDATE_ARTICLE: {
        method: 'PUT',
        url: '/articles/{article_id}',
        requiresAuth: true,
        params: {
            article_id: 'number (必填，路径参数)'
        },
        body: {
            title: 'string (可选)',
            content: 'string (可选)',
            category_id: 'number (可选)',
            tags: 'array (可选)'
        }
    }
};

// ============================================================================
// 2. API 调用标准函数
// ============================================================================

/**
 * 标准 API 调用函数
 * 
 * @param {string} method - HTTP 方法 (GET, POST, PUT, DELETE)
 * @param {string} url - API 路径 (不包含 BASE_URL)
 * @param {Object} options - 配置选项
 * @param {Object} options.params - URL 查询参数
 * @param {Object} options.body - 请求体
 * @param {boolean} options.requiresAuth - 是否需要认证
 * @param {number} options.timeout - 超时时间（毫秒）
 * @param {number} options.retryCount - 重试次数
 * @returns {Promise<Object>} API 响应数据
 */
async function callAPI(method, url, options = {}) {
    const {
        params = {},
        body = null,
        requiresAuth = false,
        timeout = CONFIG.API.TIMEOUT,
        retryCount = CONFIG.API.RETRY_COUNT
    } = options;
    
    // 构建完整的 URL
    let fullUrl = `${CONFIG.API.BASE_URL}${url}`;
    
    // 添加查询参数
    if (Object.keys(params).length > 0) {
        const queryString = new URLSearchParams(params).toString();
        fullUrl += `?${queryString}`;
    }
    
    // 准备请求头
    const headers = {
        'Content-Type': 'application/json',
    };
    
    // 添加认证令牌
    if (requiresAuth) {
        const auth = authManager.getAuth();
        if (!auth.token) {
            throw new Error('需要认证，但未找到令牌');
        }
        headers['Authorization'] = `Bearer ${auth.token}`;
    }
    
    // 准备请求配置
    const fetchOptions = {
        method,
        headers,
    };
    
    // 添加请求体（仅非 GET 请求）
    if (method !== 'GET' && body) {
        fetchOptions.body = JSON.stringify(body);
    }
    
    // 执行请求（带重试机制）
    let lastError;
    for (let i = 0; i <= retryCount; i++) {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), timeout);
            
            const response = await fetch(fullUrl, {
                ...fetchOptions,
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            // 解析响应
            const data = await response.json();
            
            // 检查响应状态
            if (!response.ok) {
                throw new APIError(response.status, data);
            }
            
            return data;
            
        } catch (error) {
            lastError = error;
            
            // 如果是 AbortError，说明超时了
            if (error.name === 'AbortError') {
                console.error(`API 调用超时：${fullUrl}`);
            }
            
            // 如果不是最后一次重试，等待一段时间后重试
            if (i < retryCount) {
                const waitTime = Math.pow(2, i) * 1000; // 指数退避
                console.warn(`API 调用失败，${waitTime/1000}秒后重试 (${i+1}/${retryCount}): ${fullUrl}`);
                await new Promise(resolve => setTimeout(resolve, waitTime));
            }
        }
    }
    
    // 所有重试都失败，抛出错误
    throw lastError;
}

// ============================================================================
// 3. 错误处理
// ============================================================================

/**
 * API 错误类
 */
class APIError extends Error {
    constructor(status, data) {
        super(data.message || data.detail || 'API 调用失败');
        this.name = 'APIError';
        this.status = status;
        this.data = data;
        this.errorCode = data.error_code || data.detail?.error_code || 'UNKNOWN_ERROR';
    }
}

/**
 * 处理 API 错误
 * 
 * @param {Error} error - 错误对象
 * @returns {Object} 错误信息
 */
function handleAPIError(error) {
    if (error instanceof APIError) {
        // API 返回的错误
        const errorInfo = {
            status: error.status,
            message: error.message,
            errorCode: error.errorCode,
        };
        
        // 根据状态码提供额外建议
        switch (error.status) {
            case 400:
                errorInfo.suggestion = '请求参数有误，请检查输入';
                break;
            case 401:
                errorInfo.suggestion = '认证失败，请重新登录';
                // 自动跳转到登录页
                setTimeout(() => {
                    window.location.href = `login.html?redirect=${encodeURIComponent(window.location.pathname)}`;
                }, 2000);
                break;
            case 403:
                errorInfo.suggestion = '没有权限执行此操作';
                break;
            case 404:
                errorInfo.suggestion = '请求的资源不存在';
                break;
            case 429:
                errorInfo.suggestion = '请求过于频繁，请稍后再试';
                break;
            case 500:
                errorInfo.suggestion = '服务器内部错误，请稍后重试';
                break;
            case 503:
                errorInfo.suggestion = '服务暂时不可用，请稍后重试';
                break;
            default:
                errorInfo.suggestion = '发生未知错误，请稍后重试';
        }
        
        return errorInfo;
    } else if (error.name === 'AbortError') {
        // 超时错误
        return {
            status: 0,
            message: '请求超时，请检查网络连接',
            errorCode: 'TIMEOUT',
            suggestion: '请检查网络连接或稍后重试'
        };
    } else {
        // 网络错误或其他错误
        return {
            status: 0,
            message: error.message || '网络错误',
            errorCode: 'NETWORK_ERROR',
            suggestion: '请检查网络连接'
        };
    }
}

// ============================================================================
// 4. 使用示例
// ============================================================================

/**
 * 示例：调用登录 API
 */
async function exampleLogin() {
    try {
        const result = await callAPI('POST', '/auth/login', {
            body: {
                username: 'testuser',
                email: 'test@example.com',
                password: 'Password123!'
            },
            requiresAuth: false
        });
        
        // 保存认证信息
        const token = result.data.access_token;
        const user = result.data.user;
        const expiry = Date.now() + (30 * 60 * 1000); // 30 分钟
        authManager.saveAuth(token, user, expiry);
        
        console.log('登录成功:', user);
        return result;
        
    } catch (error) {
        const errorInfo = handleAPIError(error);
        console.error('登录失败:', errorInfo);
        
        // 显示错误提示
        if (typeof notificationManager !== 'undefined') {
            notificationManager.error(errorInfo.message);
        }
        
        throw errorInfo;
    }
}

/**
 * 示例：获取文章列表
 */
async function exampleGetArticles() {
    try {
        const result = await callAPI('GET', '/articles', {
            params: {
                category_id: 1,
                limit: 20,
                sort_by: 'created_at',
                sort_order: 'desc'
            },
            requiresAuth: false
        });
        
        console.log('文章列表:', result.data);
        return result;
        
    } catch (error) {
        const errorInfo = handleAPIError(error);
        console.error('获取文章失败:', errorInfo);
        throw errorInfo;
    }
}

/**
 * 示例：创建文章
 */
async function exampleCreateArticle() {
    try {
        const result = await callAPI('POST', '/articles', {
            body: {
                title: '新文章标题',
                content: '文章内容...',
                category_id: 1,
                tags: [1, 2, 3]
            },
            requiresAuth: true
        });
        
        console.log('文章创建成功:', result.data);
        return result;
        
    } catch (error) {
        const errorInfo = handleAPIError(error);
        console.error('创建文章失败:', errorInfo);
        
        if (errorInfo.errorCode === 'AUTH_REQUIRED') {
            // 未认证，跳转到登录页
            window.location.href = `login.html?redirect=${encodeURIComponent(window.location.pathname)}`;
        }
        
        throw errorInfo;
    }
}

// ============================================================================
// 5. 最佳实践
// ============================================================================

/**
 * 最佳实践指南：
 * 
 * 1. 始终使用 callAPI 函数进行 API 调用，不要直接使用 fetch
 * 2. 为需要认证的接口设置 requiresAuth: true
 * 3. 使用 try-catch 块捕获和处理错误
 * 4. 使用 handleAPIError 函数统一处理错误
 * 5. 为用户提供清晰的错误提示
 * 6. 对于重要操作，添加确认步骤
 * 7. 使用通知管理器显示操作结果
 * 8. 避免频繁调用 API，注意速率限制
 * 9. 使用配置文件中定义的常量
 * 10. 记录关键 API 调用的日志（生产环境关闭）
 */

// 导出工具函数（如果在模块环境中）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        callAPI,
        handleAPIError,
        APIError,
        AUTH_APIS,
        ARTICLE_APIS,
        exampleLogin,
        exampleGetArticles,
        exampleCreateArticle
    };
}
