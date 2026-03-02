// -*- coding: utf-8 -*-
// 通用工具函数

// 登录状态管理
class AuthManager {
    constructor() {
        this.tokenKey = 'auth_token';
        this.userKey = 'user_info';
        this.expiryKey = 'token_expiry';
    }

    // 保存登录状态
    saveAuth(token, user, expiry) {
        localStorage.setItem(this.tokenKey, token);
        localStorage.setItem(this.userKey, JSON.stringify(user));
        localStorage.setItem(this.expiryKey, expiry);
    }

    // 获取登录状态
    getAuth() {
        const token = localStorage.getItem(this.tokenKey);
        const user = localStorage.getItem(this.userKey);
        const expiry = localStorage.getItem(this.expiryKey);

        return {
            token,
            user: user ? JSON.parse(user) : null,
            expiry: expiry ? parseInt(expiry) : null
        };
    }

    // 检查认证状态
    isAuthenticated() {
        const { token, expiry } = this.getAuth();
        if (!token || !expiry) return false;
        
        // 检查token是否过期
        return Date.now() < expiry;
    }

    // 注销登录
    logout() {
        localStorage.removeItem(this.tokenKey);
        localStorage.removeItem(this.userKey);
        localStorage.removeItem(this.expiryKey);
    }

    // 更新token过期时间
    updateExpiry() {
        const expiry = Date.now() + (30 * 60 * 1000); // 30分钟
        localStorage.setItem(this.expiryKey, expiry);
    }
}

// 页面状态管理
class PageStateManager {
    constructor() {
        this.stateKey = 'page_state';
        this.listeners = new Map();
        this.defaultExpiryTime = 30 * 60 * 1000; // 默认30分钟过期
    }

    // 保存页面状态
    saveState(page, state, options = {}) {
        const allStates = this.getAllStates();
        const now = Date.now();
        
        allStates[page] = {
            state,
            timestamp: now,
            accessCount: (allStates[page]?.accessCount || 0) + 1,
            lastAccessTime: now,
            expiryTime: options.expiryTime || this.defaultExpiryTime
        };
        
        localStorage.setItem(this.stateKey, JSON.stringify(allStates));
        
        // 触发状态变更事件
        this.notifyListeners(page, allStates[page]);
    }

    // 批量保存状态
    saveStates(statesMap) {
        const allStates = this.getAllStates();
        const now = Date.now();
        
        for (const [page, state] of Object.entries(statesMap)) {
            allStates[page] = {
                state,
                timestamp: now,
                accessCount: (allStates[page]?.accessCount || 0) + 1,
                lastAccessTime: now,
                expiryTime: this.defaultExpiryTime
            };
            
            // 触发状态变更事件
            this.notifyListeners(page, allStates[page]);
        }
        
        localStorage.setItem(this.stateKey, JSON.stringify(allStates));
    }

    // 获取页面状态
    getState(page, options = {}) {
        const allStates = this.getAllStates();
        const pageState = allStates[page];
        
        if (!pageState) {
            return null;
        }
        
        const now = Date.now();
        const expiryTime = options.expiryTime || pageState.expiryTime || this.defaultExpiryTime;
        
        // 检查状态是否过期
        if (now - pageState.timestamp > expiryTime) {
            // 自动清理过期状态
            this.clearState(page);
            return null;
        }
        
        // 更新最后访问时间和访问次数
        pageState.lastAccessTime = now;
        pageState.accessCount = (pageState.accessCount || 0) + 1;
        localStorage.setItem(this.stateKey, JSON.stringify(allStates));
        
        return pageState.state;
    }

    // 批量获取状态
    getStates(pages, options = {}) {
        const result = {};
        const allStates = this.getAllStates();
        
        for (const page of pages) {
            const pageState = allStates[page];
            if (pageState) {
                const now = Date.now();
                const expiryTime = options.expiryTime || pageState.expiryTime || this.defaultExpiryTime;
                
                if (now - pageState.timestamp <= expiryTime) {
                    result[page] = pageState.state;
                    
                    // 更新最后访问时间和访问次数
                    pageState.lastAccessTime = now;
                    pageState.accessCount = (pageState.accessCount || 0) + 1;
                } else {
                    // 自动清理过期状态
                    this.clearState(page);
                }
            }
        }
        
        localStorage.setItem(this.stateKey, JSON.stringify(allStates));
        return result;
    }

    // 获取所有状态（包含元数据）
    getAllStates() {
        const states = localStorage.getItem(this.stateKey);
        return states ? JSON.parse(states) : {};
    }

    // 获取活跃状态（未过期的）
    getActiveStates(options = {}) {
        const allStates = this.getAllStates();
        const activeStates = {};
        const now = Date.now();
        
        for (const [page, pageState] of Object.entries(allStates)) {
            const expiryTime = options.expiryTime || pageState.expiryTime || this.defaultExpiryTime;
            if (now - pageState.timestamp <= expiryTime) {
                activeStates[page] = pageState;
            }
        }
        
        return activeStates;
    }

    // 清除页面状态
    clearState(page) {
        const allStates = this.getAllStates();
        delete allStates[page];
        localStorage.setItem(this.stateKey, JSON.stringify(allStates));
        
        // 触发状态变更事件（清除状态）
        this.notifyListeners(page, null);
    }

    // 清除多个状态
    clearStates(pages) {
        const allStates = this.getAllStates();
        
        for (const page of pages) {
            delete allStates[page];
            // 触发状态变更事件（清除状态）
            this.notifyListeners(page, null);
        }
        
        localStorage.setItem(this.stateKey, JSON.stringify(allStates));
    }

    // 清除过期状态
    clearExpiredStates(options = {}) {
        const allStates = this.getAllStates();
        const now = Date.now();
        const statesToClear = [];
        
        for (const [page, pageState] of Object.entries(allStates)) {
            const expiryTime = options.expiryTime || pageState.expiryTime || this.defaultExpiryTime;
            if (now - pageState.timestamp > expiryTime) {
                statesToClear.push(page);
            }
        }
        
        this.clearStates(statesToClear);
        return statesToClear.length;
    }

    // 清除所有状态
    clearAllStates() {
        const allStates = this.getAllStates();
        
        // 触发所有状态变更事件（清除状态）
        for (const page of Object.keys(allStates)) {
            this.notifyListeners(page, null);
        }
        
        localStorage.removeItem(this.stateKey);
    }

    // 添加状态变更监听器
    onStateChange(page, callback) {
        if (!this.listeners.has(page)) {
            this.listeners.set(page, []);
        }
        this.listeners.get(page).push(callback);
    }

    // 移除状态变更监听器
    offStateChange(page, callback) {
        if (this.listeners.has(page)) {
            const callbacks = this.listeners.get(page).filter(cb => cb !== callback);
            if (callbacks.length > 0) {
                this.listeners.set(page, callbacks);
            } else {
                this.listeners.delete(page);
            }
        }
    }

    // 通知状态变更
    notifyListeners(page, newState) {
        if (this.listeners.has(page)) {
            const callbacks = this.listeners.get(page);
            for (const callback of callbacks) {
                callback(newState);
            }
        }
    }

    // 获取状态统计信息
    getStateStats(page) {
        const allStates = this.getAllStates();
        const pageState = allStates[page];
        
        if (!pageState) {
            return null;
        }
        
        return {
            page,
            accessCount: pageState.accessCount || 0,
            createdAt: pageState.timestamp,
            lastAccessTime: pageState.lastAccessTime || pageState.timestamp,
            age: Date.now() - pageState.timestamp
        };
    }
}

// 表单数据管理
class FormManager {
    constructor() {
        this.formKey = 'form_data';
    }

    // 保存表单数据
    saveFormData(formId, data) {
        const allFormData = this.getAllFormData();
        allFormData[formId] = {
            data,
            timestamp: Date.now()
        };
        localStorage.setItem(this.formKey, JSON.stringify(allFormData));
    }

    // 获取表单数据
    getFormData(formId) {
        const allFormData = this.getAllFormData();
        return allFormData[formId] || null;
    }

    // 获取所有表单数据
    getAllFormData() {
        const formData = localStorage.getItem(this.formKey);
        return formData ? JSON.parse(formData) : {};
    }

    // 清除表单数据
    clearFormData(formId) {
        const allFormData = this.getAllFormData();
        delete allFormData[formId];
        localStorage.setItem(this.formKey, JSON.stringify(allFormData));
    }

    // 清除所有表单数据
    clearAllFormData() {
        localStorage.removeItem(this.formKey);
    }

    // 从表单元素中提取数据
    extractFormData(formElement) {
        const data = {};
        const elements = formElement.elements;
        
        for (let i = 0; i < elements.length; i++) {
            const element = elements[i];
            if (element.name && element.type !== 'submit' && element.type !== 'button') {
                if (element.type === 'checkbox') {
                    data[element.name] = element.checked;
                } else if (element.type === 'radio' && element.checked) {
                    data[element.name] = element.value;
                } else {
                    data[element.name] = element.value;
                }
            }
        }
        
        return data;
    }

    // 将数据填充到表单中
    populateForm(formElement, data) {
        for (const [key, value] of Object.entries(data)) {
            const element = formElement.elements[key];
            if (element) {
                if (element.type === 'checkbox') {
                    element.checked = value;
                } else if (element.type === 'radio') {
                    const radioElements = formElement.querySelectorAll(`[name="${key}"]`);
                    radioElements.forEach(radio => {
                        radio.checked = radio.value === value;
                    });
                } else {
                    element.value = value;
                }
            }
        }
    }
}

// 路由管理器
class RouterManager {
    constructor() {
        this.routes = {};
        this.beforeEachHooks = [];
        this.afterEachHooks = [];
    }

    // 注册路由
    registerRoute(name, path, options = {}) {
        this.routes[name] = {
            path,
            ...options
        };
    }

    // 注册多个路由
    registerRoutes(routes) {
        for (const [name, config] of Object.entries(routes)) {
            this.registerRoute(name, config.path, config);
        }
    }

    // 获取路由配置
    getRoute(name) {
        return this.routes[name];
    }

    // 获取当前路由
    getCurrentRoute() {
        const path = window.location.pathname;
        for (const [name, route] of Object.entries(this.routes)) {
            if (route.path === path) {
                return { name, ...route };
            }
        }
        return null;
    }

    // 路由跳转
    push(name, params = {}) {
        const route = this.getRoute(name);
        if (!route) {
            console.error(`Route ${name} not found`);
            return;
        }

        // 构建URL
        let url = route.path;
        if (params) {
            const queryString = new URLSearchParams(params).toString();
            if (queryString) {
                url += `?${queryString}`;
            }
        }

        // 执行前置守卫
        const canNavigate = this.executeBeforeEachHooks(name, params);
        if (!canNavigate) {
            return;
        }

        // 跳转到新页面
        window.location.href = url;
    }

    // 替换当前页面
    replace(name, params = {}) {
        const route = this.getRoute(name);
        if (!route) {
            console.error(`Route ${name} not found`);
            return;
        }

        // 构建URL
        let url = route.path;
        if (params) {
            const queryString = new URLSearchParams(params).toString();
            if (queryString) {
                url += `?${queryString}`;
            }
        }

        // 执行前置守卫
        const canNavigate = this.executeBeforeEachHooks(name, params);
        if (!canNavigate) {
            return;
        }

        // 替换当前页面
        window.location.replace(url);
    }

    // 返回上一页
    goBack() {
        window.history.back();
    }

    // 前进一页
    goForward() {
        window.history.forward();
    }

    // 跳转到指定历史记录
    go(delta) {
        window.history.go(delta);
    }

    // 添加前置守卫
    beforeEach(hook) {
        this.beforeEachHooks.push(hook);
    }

    // 添加后置守卫
    afterEach(hook) {
        this.afterEachHooks.push(hook);
    }

    // 执行前置守卫
    executeBeforeEachHooks(routeName, params) {
        for (const hook of this.beforeEachHooks) {
            if (hook(routeName, params) === false) {
                return false;
            }
        }
        return true;
    }

    // 执行后置守卫
    executeAfterEachHooks(routeName, params) {
        for (const hook of this.afterEachHooks) {
            hook(routeName, params);
        }
    }

    // 解析URL参数
    parseQueryParams() {
        const params = {};
        const urlParams = new URLSearchParams(window.location.search);
        for (const [key, value] of urlParams) {
            params[key] = value;
        }
        return params;
    }

    // 获取指定URL参数
    getQueryParam(key) {
        return new URLSearchParams(window.location.search).get(key);
    }

    // 构建URL
    buildUrl(name, params = {}) {
        const route = this.getRoute(name);
        if (!route) {
            console.error(`Route ${name} not found`);
            return '';
        }

        let url = route.path;
        if (params) {
            const queryString = new URLSearchParams(params).toString();
            if (queryString) {
                url += `?${queryString}`;
            }
        }
        return url;
    }
}

// 导航管理器
class NavigationManager {
    constructor() {
        this.breadcrumbKey = 'breadcrumb';
        this.maxBreadcrumbItems = 5;
    }

    // 添加面包屑项
    addBreadcrumbItem(label, url) {
        const breadcrumb = this.getBreadcrumb();
        
        // 移除重复项
        const filteredBreadcrumb = breadcrumb.filter(item => item.url !== url);
        
        // 添加新项
        filteredBreadcrumb.push({ label, url });
        
        // 限制数量
        if (filteredBreadcrumb.length > this.maxBreadcrumbItems) {
            filteredBreadcrumb.shift();
        }
        
        localStorage.setItem(this.breadcrumbKey, JSON.stringify(filteredBreadcrumb));
    }

    // 获取面包屑
    getBreadcrumb() {
        const breadcrumb = localStorage.getItem(this.breadcrumbKey);
        return breadcrumb ? JSON.parse(breadcrumb) : [];
    }

    // 清除面包屑
    clearBreadcrumb() {
        localStorage.removeItem(this.breadcrumbKey);
    }

    // 渲染面包屑
    renderBreadcrumb(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        const breadcrumb = this.getBreadcrumb();
        if (breadcrumb.length === 0) {
            container.innerHTML = '<span class="breadcrumb-item">首页</span>';
            return;
        }
        
        let html = '<a href="index.html" class="breadcrumb-item">首页</a>';
        breadcrumb.forEach((item, index) => {
            if (index === breadcrumb.length - 1) {
                html += `<span class="breadcrumb-separator">/</span>`;
                html += `<span class="breadcrumb-item active">${item.label}</span>`;
            } else {
                html += `<span class="breadcrumb-separator">/</span>`;
                html += `<a href="${item.url}" class="breadcrumb-item">${item.label}</a>`;
            }
        });
        
        container.innerHTML = html;
    }
}

// 加载状态管理器
class LoadingManager {
    constructor() {
        this.loadingElements = new Map();
    }

    // 显示加载状态
    showLoading(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.style.display = 'block';
            this.loadingElements.set(elementId, element);
        }
    }

    // 隐藏加载状态
    hideLoading(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.style.display = 'none';
            this.loadingElements.delete(elementId);
        }
    }

    // 隐藏所有加载状态
    hideAllLoading() {
        this.loadingElements.forEach((element, id) => {
            element.style.display = 'none';
        });
        this.loadingElements.clear();
    }
}

// 通知管理器
class NotificationManager {
    constructor() {
        this.containerId = 'notification-container';
        this.createContainer();
    }

    // 创建通知容器
    createContainer() {
        let container = document.getElementById(this.containerId);
        if (!container) {
            container = document.createElement('div');
            container.id = this.containerId;
            container.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 10000;
                display: flex;
                flex-direction: column;
                gap: 10px;
            `;
            
            // 确保 body 存在后再添加
            if (document.body) {
                document.body.appendChild(container);
            } else {
                // 如果 body 还不存在，等待 DOM 加载完成
                document.addEventListener('DOMContentLoaded', () => {
                    document.body.appendChild(container);
                });
            }
        }
    }

    // 显示通知
    show(message, type = 'success', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.style.cssText = `
            padding: 12px 20px;
            border-radius: 4px;
            color: white;
            font-weight: 500;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            animation: slideInRight 0.3s ease-out;
            background: ${type === 'success' ? 'rgba(0, 255, 157, 0.9)' : 
                        type === 'error' ? 'rgba(255, 68, 68, 0.9)' : 
                        type === 'warning' ? 'rgba(255, 170, 0, 0.9)' : 
                        'rgba(0, 204, 255, 0.9)'};
        `;
        notification.textContent = message;
        
        const container = document.getElementById(this.containerId);
        if (container) {
            container.appendChild(notification);
            
            // 自动关闭
            setTimeout(() => {
                notification.style.animation = 'slideOutRight 0.3s ease-out';
                setTimeout(() => {
                    notification.remove();
                }, 300);
            }, duration);
        } else {
            // 如果容器不存在，延迟后重试
            setTimeout(() => this.show(message, type, duration), 100);
        }
    }

    // 显示成功通知
    success(message, duration = 3000) {
        this.show(message, 'success', duration);
    }

    // 显示错误通知
    error(message, duration = 5000) {
        this.show(message, 'error', duration);
    }

    // 显示警告通知
    warning(message, duration = 4000) {
        this.show(message, 'warning', duration);
    }

    // 显示信息通知
    info(message, duration = 3000) {
        this.show(message, 'info', duration);
    }
}

// 初始化所有管理器
const authManager = new AuthManager();
const pageStateManager = new PageStateManager();
const formManager = new FormManager();
const navigationManager = new NavigationManager();
const loadingManager = new LoadingManager();
const notificationManager = new NotificationManager();
const routerManager = new RouterManager();

// 配置路由守卫
routerManager.beforeEach((routeName, params) => {
    const route = routerManager.getRoute(routeName);
    if (!route) {
        return true;
    }

    // 检查是否需要认证
    if (route.requiresAuth) {
        if (!authManager.isAuthenticated()) {
            notificationManager.warning('请先登录');
            routerManager.push('login', { redirect: window.location.pathname });
            return false;
        }
    }

    // 检查是否需要管理员权限
    if (route.requiresAdmin) {
        const user = authManager.getAuth().user;
        if (!user || !user.is_admin) {
            notificationManager.error('需要管理员权限');
            routerManager.push('home');
            return false;
        }
    }

    return true;
});

// 注册默认路由
routerManager.registerRoutes({
    home: {
        path: '/index.html',
        label: '首页'
    },
    articles: {
        path: '/articles.html',
        label: '文章列表'
    },
    articleDetail: {
        path: '/article-detail.html',
        label: '文章详情'
    },
    categories: {
        path: '/categories.html',
        label: '分类'
    },
    categoryArticles: {
        path: '/category-articles.html',
        label: '分类文章'
    },
    createArticle: {
        path: '/create-article.html',
        label: '创建文章',
        requiresAuth: true
    },
    editArticle: {
        path: '/edit-article.html',
        label: '编辑文章',
        requiresAuth: true
    },
    login: {
        path: '/login.html',
        label: '登录'
    },
    register: {
        path: '/register.html',
        label: '注册'
    },
    metro: {
        path: '/metro.html',
        label: '地铁'
    },
    music: {
        path: '/music.html',
        label: '音乐'
    },
    profile: {
        path: '/profile.html',
        label: '个人资料',
        requiresAuth: true
    },
    search: {
        path: '/search.html',
        label: '搜索'
    },
    tagArticles: {
        path: '/tag-articles.html',
        label: '标签文章'
    },
    userProfile: {
        path: '/user-profile.html',
        label: '用户资料'
    },
    // 管理员路由
    adminDashboard: {
        path: '/admin-dashboard.html',
        label: '管理面板',
        requiresAuth: true,
        requiresAdmin: true
    },
    adminArticles: {
        path: '/admin-articles.html',
        label: '管理文章',
        requiresAuth: true,
        requiresAdmin: true
    },
    adminComments: {
        path: '/admin-comments.html',
        label: '管理评论',
        requiresAuth: true,
        requiresAdmin: true
    },
    adminModeration: {
        path: '/admin-moderation.html',
        label: '内容审核',
        requiresAuth: true,
        requiresAdmin: true
    },
    adminUsers: {
        path: '/admin-users.html',
        label: '管理用户',
        requiresAuth: true,
        requiresAdmin: true
    }
});

// 页面过渡动画
function addPageTransition() {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.3s ease-in-out';
    
    window.addEventListener('load', () => {
        document.body.style.opacity = '1';
    });
    
    // 为所有链接添加过渡效果
    document.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', (e) => {
            // 只处理同域链接
            if (link.hostname === window.location.hostname) {
                e.preventDefault();
                const href = link.getAttribute('href');
                
                document.body.style.opacity = '0';
                setTimeout(() => {
                    window.location.href = href;
                }, 300);
            }
        });
    });
}

// 添加CSS动画
function addAnimations() {
    const style = document.createElement('style');
    style.textContent = `
        /* 页面过渡动画 */
        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOutRight {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        
        @keyframes fadeOut {
            from {
                opacity: 1;
            }
            to {
                opacity: 0;
            }
        }
        
        /* 加载动画 */
        @keyframes spin {
            to {
                transform: rotate(360deg);
            }
        }
        
        /* 按钮呼吸动画 */
        @keyframes pulse {
            0% {
                box-shadow: 0 0 0 0 rgba(0, 255, 157, 0.4);
            }
            70% {
                box-shadow: 0 0 0 10px rgba(0, 255, 157, 0);
            }
            100% {
                box-shadow: 0 0 0 0 rgba(0, 255, 157, 0);
            }
        }
        
        /* 面包屑样式 */
        .breadcrumb {
            margin-bottom: 20px;
            padding: 10px 0;
            border-bottom: 1px solid var(--color-border);
        }
        
        .breadcrumb-item {
            color: var(--color-text-muted);
            text-decoration: none;
            transition: all 0.2s;
        }
        
        .breadcrumb-item:hover {
            color: var(--color-primary);
        }
        
        .breadcrumb-item.active {
            color: var(--color-primary);
            font-weight: 500;
        }
        
        .breadcrumb-separator {
            margin: 0 8px;
            color: var(--color-text-muted);
        }
        
        /* 登录状态指示器 */
        .auth-indicator {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .auth-status {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--color-primary);
            animation: pulse 2s infinite;
        }
        
        /* 响应式设置 */
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .hero {
                padding: 40px 10px;
            }
            
            .hero h1 {
                font-size: 2rem;
            }
            
            .search-section {
                flex-direction: column;
            }
        }
        
        /* 加载状态样式 */
        .loading {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 60px;
            color: var(--color-text-muted);
        }
        
        .loading-spinner {
            width: 40px;
            height: 40px;
            border: 3px solid var(--color-border);
            border-top-color: var(--color-primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 16px;
        }
        
        /* 按钮交互动效 */
        button, .btn {
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        button:hover, .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 255, 157, 0.2);
        }
        
        button:active, .btn:active {
            transform: translateY(0);
        }
        
        /* 表单元素交互 */
        input, textarea, select {
            transition: all 0.3s ease;
        }
        
        input:focus, textarea:focus, select:focus {
            outline: none;
            box-shadow: 0 0 10px rgba(0, 255, 157, 0.2);
            border-color: var(--color-primary);
        }
        
        /* 通知样式 */
        .notification {
            padding: 12px 20px;
            border-radius: 4px;
            color: white;
            font-weight: 500;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            animation: slideInRight 0.3s ease-out;
        }
        
        .notification-success {
            background: rgba(0, 255, 157, 0.9);
            border-left: 4px solid var(--color-primary);
        }
        
        .notification-error {
            background: rgba(255, 68, 68, 0.9);
            border-left: 4px solid #ff4444;
        }
        
        .notification-warning {
            background: rgba(255, 170, 0, 0.9);
            border-left: 4px solid #ffaa00;
        }
        
        .notification-info {
            background: rgba(0, 204, 255, 0.9);
            border-left: 4px solid var(--color-secondary);
        }
    `;
    document.head.appendChild(style);
}

// 初始化页面
function initPage(pageName, pageLabel) {
    // 添加页面过渡动画
    addPageTransition();
    
    // 添加CSS动画
    addAnimations();
    
    // 添加面包屑
    navigationManager.addBreadcrumbItem(pageLabel, window.location.pathname);
    
    // 渲染面包屑
    const breadcrumbContainer = document.getElementById('breadcrumb');
    if (breadcrumbContainer) {
        navigationManager.renderBreadcrumb('breadcrumb');
    }
    
    // 检查认证状态
    if (authManager.isAuthenticated()) {
        // 更新token过期时间
        authManager.updateExpiry();
        
        // 显示登录状态
        const authIndicator = document.getElementById('auth-indicator');
        if (authIndicator) {
            const user = authManager.getAuth().user;
            authIndicator.innerHTML = `
                <div class="auth-status"></div>
                <span>${user.username}</span>
            `;
        }
    } else {
        // 清除过期的登录状态
        authManager.logout();
    }
    
    // 保存页面状态
    window.addEventListener('beforeunload', () => {
        const state = {
            scrollY: window.scrollY || window.pageYOffset || 0,
            timestamp: Date.now()
        };
        pageStateManager.saveState(pageName, state);
    });
    
    // 恢复页面状态
    window.addEventListener('load', () => {
        const savedState = pageStateManager.getState(pageName);
        if (savedState && savedState.state) {
            // 只恢复最近 5 分钟的状态
            if (Date.now() - savedState.timestamp < 5 * 60 * 1000) {
                const scrollY = savedState.state.scrollY || 0;
                window.scrollTo(0, scrollY);
            }
        }
    });
}

// 导出全局变量
window.authManager = authManager;
window.pageStateManager = pageStateManager;
window.formManager = formManager;
window.navigationManager = navigationManager;
window.loadingManager = loadingManager;
window.notificationManager = notificationManager;
window.routerManager = routerManager;
window.initPage = initPage;