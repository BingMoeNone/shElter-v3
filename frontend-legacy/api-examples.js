/**
 * API 调用示例文件
 * 展示如何在实际项目中使用标准化的 API 调用方式
 */

// ============================================================================
// 示例 1: 用户登录
// ============================================================================

/**
 * 用户登录函数
 * @param {string} username - 用户名
 * @param {string} email - 邮箱
 * @param {string} password - 密码
 * @returns {Promise<Object>} 登录结果
 */
async function loginUser(username, email, password) {
    try {
        // 使用标准化的 API 调用函数
        const result = await callAPI('POST', '/auth/login', {
            body: {
                username: username,
                email: email,
                password: password
            },
            requiresAuth: false,
            timeout: CONFIG.API.TIMEOUT,
            retryCount: CONFIG.API.RETRY_COUNT
        });
        
        // 提取令牌和用户信息
        const token = result.data?.access_token || result.access_token;
        const user = result.data?.user || result.user;
        
        // 保存认证信息
        const expiry = Date.now() + (30 * 60 * 1000); // 30 分钟
        authManager.saveAuth(token, user, expiry);
        
        // 显示成功通知
        if (typeof notificationManager !== 'undefined') {
            notificationManager.success('登录成功！');
        }
        
        return result;
        
    } catch (error) {
        // 处理错误
        const errorInfo = handleAPIError(error);
        
        // 显示错误通知
        if (typeof notificationManager !== 'undefined') {
            notificationManager.error(errorInfo.message);
        }
        
        // 记录错误日志
        if (CONFIG.FEATURES.ENABLE_LOGGING) {
            console.error('登录失败:', errorInfo);
        }
        
        throw errorInfo;
    }
}

// ============================================================================
// 示例 2: 获取文章列表
// ============================================================================

/**
 * 获取文章列表
 * @param {Object} params - 查询参数
 * @returns {Promise<Object>} 文章列表
 */
async function getArticles(params = {}) {
    try {
        const result = await callAPI('GET', '/articles', {
            params: {
                title: params.title || undefined,
                category_id: params.categoryId || undefined,
                tag_id: params.tagId || undefined,
                author_id: params.authorId || undefined,
                skip: params.skip || 0,
                limit: params.limit || CONFIG.PAGINATION.DEFAULT_PAGE_SIZE,
                sort_by: params.sortBy || 'created_at',
                sort_order: params.sortOrder || 'desc'
            },
            requiresAuth: false
        });
        
        if (CONFIG.FEATURES.ENABLE_LOGGING) {
            console.log('获取文章列表成功:', result.data);
        }
        
        return result;
        
    } catch (error) {
        const errorInfo = handleAPIError(error);
        
        if (CONFIG.FEATURES.ENABLE_LOGGING) {
            console.error('获取文章列表失败:', errorInfo);
        }
        
        throw errorInfo;
    }
}

// ============================================================================
// 示例 3: 获取文章详情
// ============================================================================

/**
 * 获取文章详情
 * @param {number} articleId - 文章 ID
 * @returns {Promise<Object>} 文章详情
 */
async function getArticleDetail(articleId) {
    try {
        const result = await callAPI('GET', `/articles/${articleId}`, {
            requiresAuth: false
        });
        
        if (CONFIG.FEATURES.ENABLE_LOGGING) {
            console.log('获取文章详情成功:', result.data);
        }
        
        return result;
        
    } catch (error) {
        const errorInfo = handleAPIError(error);
        
        if (CONFIG.FEATURES.ENABLE_LOGGING) {
            console.error('获取文章详情失败:', errorInfo);
        }
        
        throw errorInfo;
    }
}

// ============================================================================
// 示例 4: 创建文章
// ============================================================================

/**
 * 创建文章
 * @param {Object} articleData - 文章数据
 * @returns {Promise<Object>} 创建的文章
 */
async function createArticle(articleData) {
    try {
        const result = await callAPI('POST', '/articles', {
            body: {
                title: articleData.title,
                content: articleData.content,
                category_id: articleData.categoryId,
                tags: articleData.tags || []
            },
            requiresAuth: true
        });
        
        // 显示成功通知
        if (typeof notificationManager !== 'undefined') {
            notificationManager.success('文章创建成功！');
        }
        
        if (CONFIG.FEATURES.ENABLE_LOGGING) {
            console.log('创建文章成功:', result.data);
        }
        
        return result;
        
    } catch (error) {
        const errorInfo = handleAPIError(error);
        
        // 如果是认证错误，跳转到登录页
        if (errorInfo.errorCode === 'AUTH_REQUIRED' || errorInfo.status === 401) {
            if (typeof notificationManager !== 'undefined') {
                notificationManager.error('请先登录');
            }
            setTimeout(() => {
                window.location.href = `login.html?redirect=${encodeURIComponent(window.location.pathname)}`;
            }, 2000);
            return;
        }
        
        // 显示错误通知
        if (typeof notificationManager !== 'undefined') {
            notificationManager.error(errorInfo.message);
        }
        
        if (CONFIG.FEATURES.ENABLE_LOGGING) {
            console.error('创建文章失败:', errorInfo);
        }
        
        throw errorInfo;
    }
}

// ============================================================================
// 示例 5: 更新文章
// ============================================================================

/**
 * 更新文章
 * @param {number} articleId - 文章 ID
 * @param {Object} articleData - 更新的文章数据
 * @returns {Promise<Object>} 更新后的文章
 */
async function updateArticle(articleId, articleData) {
    try {
        const result = await callAPI('PUT', `/articles/${articleId}`, {
            body: {
                title: articleData.title,
                content: articleData.content,
                category_id: articleData.categoryId,
                tags: articleData.tags || []
            },
            requiresAuth: true
        });
        
        // 显示成功通知
        if (typeof notificationManager !== 'undefined') {
            notificationManager.success('文章更新成功！');
        }
        
        if (CONFIG.FEATURES.ENABLE_LOGGING) {
            console.log('更新文章成功:', result.data);
        }
        
        return result;
        
    } catch (error) {
        const errorInfo = handleAPIError(error);
        
        // 如果是权限错误
        if (errorInfo.status === 403) {
            if (typeof notificationManager !== 'undefined') {
                notificationManager.error('没有权限修改该文章');
            }
        } else {
            if (typeof notificationManager !== 'undefined') {
                notificationManager.error(errorInfo.message);
            }
        }
        
        if (CONFIG.FEATURES.ENABLE_LOGGING) {
            console.error('更新文章失败:', errorInfo);
        }
        
        throw errorInfo;
    }
}

// ============================================================================
// 示例 6: 在 HTML 页面中使用
// ============================================================================

/**
 * 在 HTML 页面中使用的完整示例
 * 这个函数展示了如何在实际的 HTML 页面中集成 API 调用
 */
async function exampleInHTMLPage() {
    // 假设这是在 articles.html 页面中
    
    // 1. 页面加载时获取文章列表
    async function loadArticles() {
        // 显示加载状态
        const loadingElement = document.getElementById('loading');
        if (loadingElement) {
            loadingElement.style.display = 'flex';
        }
        
        try {
            const articles = await getArticles({
                limit: 20,
                sortBy: 'created_at',
                sortOrder: 'desc'
            });
            
            // 渲染文章列表
            renderArticles(articles.data);
            
        } catch (error) {
            // 显示错误状态
            showError('加载文章失败：' + error.message);
        } finally {
            // 隐藏加载状态
            if (loadingElement) {
                loadingElement.style.display = 'none';
            }
        }
    }
    
    // 2. 处理搜索
    async function handleSearch(query) {
        try {
            const articles = await getArticles({
                title: query,
                limit: 20
            });
            
            renderArticles(articles.data);
            
        } catch (error) {
            if (typeof notificationManager !== 'undefined') {
                notificationManager.error('搜索失败：' + error.message);
            }
        }
    }
    
    // 3. 处理分页
    async function handlePageChange(page, pageSize) {
        try {
            const articles = await getArticles({
                skip: (page - 1) * pageSize,
                limit: pageSize
            });
            
            renderArticles(articles.data);
            
        } catch (error) {
            if (typeof notificationManager !== 'undefined') {
                notificationManager.error('加载失败：' + error.message);
            }
        }
    }
    
    // 4. 渲染文章列表
    function renderArticles(articles) {
        const container = document.getElementById('articles-list');
        if (!container) return;
        
        container.innerHTML = articles.map(article => `
            <div class="article-card">
                <h2>${article.title}</h2>
                <p>${article.excerpt || ''}</p>
                <div class="meta">
                    <span>作者：${article.author?.username || '未知'}</span>
                    <span>发布时间：${new Date(article.created_at).toLocaleDateString('zh-CN')}</span>
                    <span>浏览：${article.views || 0}</span>
                </div>
            </div>
        `).join('');
    }
    
    // 5. 显示错误信息
    function showError(message) {
        const errorElement = document.getElementById('error-message');
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
        }
    }
    
    // 页面加载时执行
    document.addEventListener('DOMContentLoaded', loadArticles);
}

// ============================================================================
// 示例 7: 使用缓存优化性能
// ============================================================================

/**
 * 带缓存的文章列表获取
 * @param {Object} params - 查询参数
 * @param {boolean} forceRefresh - 是否强制刷新
 * @returns {Promise<Object>} 文章列表
 */
async function getArticlesWithCache(params = {}, forceRefresh = false) {
    const cacheKey = 'articles_' + JSON.stringify(params);
    
    // 检查缓存
    if (!forceRefresh && CONFIG.CACHE.ENABLE_CACHE) {
        const cached = localStorage.getItem(cacheKey);
        if (cached) {
            const { data, timestamp } = JSON.parse(cached);
            const now = Date.now();
            
            // 检查缓存是否过期
            if (now - timestamp < CONFIG.CACHE.ARTICLES_TTL) {
                if (CONFIG.FEATURES.ENABLE_LOGGING) {
                    console.log('使用缓存数据:', cacheKey);
                }
                return data;
            }
        }
    }
    
    // 从 API 获取数据
    const result = await getArticles(params);
    
    // 保存到缓存
    if (CONFIG.CACHE.ENABLE_CACHE) {
        localStorage.setItem(cacheKey, JSON.stringify({
            data: result,
            timestamp: Date.now()
        }));
    }
    
    return result;
}

// ============================================================================
// 导出所有示例函数
// ============================================================================

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        loginUser,
        getArticles,
        getArticleDetail,
        createArticle,
        updateArticle,
        getArticlesWithCache,
        exampleInHTMLPage
    };
}
