// 閫氱敤宸ュ叿鍑芥暟

// 鐧诲綍鐘舵€佺鐞?class AuthManager {
    constructor() {
        this.tokenKey = 'auth_token';
        this.userKey = 'user_info';
        this.expiryKey = 'token_expiry';
    }

    // 淇濆瓨鐧诲綍鐘舵€?    saveAuth(token, user, expiry) {
        localStorage.setItem(this.tokenKey, token);
        localStorage.setItem(this.userKey, JSON.stringify(user));
        localStorage.setItem(this.expiryKey, expiry);
    }

    // 鑾峰彇鐧诲綍鐘舵€?    getAuth() {
        const token = localStorage.getItem(this.tokenKey);
        const user = localStorage.getItem(this.userKey);
        const expiry = localStorage.getItem(this.expiryKey);

        return {
            token,
            user: user ? JSON.parse(user) : null,
            expiry: expiry ? parseInt(expiry) : null
        };
    }

    // 妫€鏌ョ櫥褰曠姸鎬?    isAuthenticated() {
        const { token, expiry } = this.getAuth();
        if (!token || !expiry) return false;
        
        // 妫€鏌oken鏄惁杩囨湡
        return Date.now() < expiry;
    }

    // 娉ㄩ攢鐧诲綍
    logout() {
        localStorage.removeItem(this.tokenKey);
        localStorage.removeItem(this.userKey);
        localStorage.removeItem(this.expiryKey);
    }

    // 鏇存柊token杩囨湡鏃堕棿
    updateExpiry() {
        const expiry = Date.now() + (30 * 60 * 1000); // 30鍒嗛挓
        localStorage.setItem(this.expiryKey, expiry);
    }
}

// 椤甸潰鐘舵€佺鐞?class PageStateManager {
    constructor() {
        this.stateKey = 'page_state';
    }

    // 淇濆瓨椤甸潰鐘舵€?    saveState(page, state) {
        const allStates = this.getAllStates();
        allStates[page] = {
            state,
            timestamp: Date.now()
        };
        localStorage.setItem(this.stateKey, JSON.stringify(allStates));
    }

    // 鑾峰彇椤甸潰鐘舵€?    getState(page) {
        const allStates = this.getAllStates();
        return allStates[page] || null;
    }

    // 鑾峰彇鎵€鏈夌姸鎬?    getAllStates() {
        const states = localStorage.getItem(this.stateKey);
        return states ? JSON.parse(states) : {};
    }

    // 娓呴櫎椤甸潰鐘舵€?    clearState(page) {
        const allStates = this.getAllStates();
        delete allStates[page];
        localStorage.setItem(this.stateKey, JSON.stringify(allStates));
    }

    // 娓呴櫎鎵€鏈夌姸鎬?    clearAllStates() {
        localStorage.removeItem(this.stateKey);
    }
}

// 琛ㄥ崟鏁版嵁绠＄悊
class FormManager {
    constructor() {
        this.formKey = 'form_data';
    }

    // 淇濆瓨琛ㄥ崟鏁版嵁
    saveFormData(formId, data) {
        const allFormData = this.getAllFormData();
        allFormData[formId] = {
            data,
            timestamp: Date.now()
        };
        localStorage.setItem(this.formKey, JSON.stringify(allFormData));
    }

    // 鑾峰彇琛ㄥ崟鏁版嵁
    getFormData(formId) {
        const allFormData = this.getAllFormData();
        return allFormData[formId] || null;
    }

    // 鑾峰彇鎵€鏈夎〃鍗曟暟鎹?    getAllFormData() {
        const formData = localStorage.getItem(this.formKey);
        return formData ? JSON.parse(formData) : {};
    }

    // 娓呴櫎琛ㄥ崟鏁版嵁
    clearFormData(formId) {
        const allFormData = this.getAllFormData();
        delete allFormData[formId];
        localStorage.setItem(this.formKey, JSON.stringify(allFormData));
    }

    // 娓呴櫎鎵€鏈夎〃鍗曟暟鎹?    clearAllFormData() {
        localStorage.removeItem(this.formKey);
    }

    // 浠庤〃鍗曞厓绱犱腑鎻愬彇鏁版嵁
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

    // 灏嗘暟鎹～鍏呭埌琛ㄥ崟涓?    populateForm(formElement, data) {
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

// 瀵艰埅绠＄悊鍣?class NavigationManager {
    constructor() {
        this.breadcrumbKey = 'breadcrumb';
        this.maxBreadcrumbItems = 5;
    }

    // 娣诲姞闈㈠寘灞戦」
    addBreadcrumbItem(label, url) {
        const breadcrumb = this.getBreadcrumb();
        
        // 绉婚櫎閲嶅椤?        const filteredBreadcrumb = breadcrumb.filter(item => item.url !== url);
        
        // 娣诲姞鏂伴」
        filteredBreadcrumb.push({ label, url });
        
        // 闄愬埗鏁伴噺
        if (filteredBreadcrumb.length > this.maxBreadcrumbItems) {
            filteredBreadcrumb.shift();
        }
        
        localStorage.setItem(this.breadcrumbKey, JSON.stringify(filteredBreadcrumb));
    }

    // 鑾峰彇闈㈠寘灞?    getBreadcrumb() {
        const breadcrumb = localStorage.getItem(this.breadcrumbKey);
        return breadcrumb ? JSON.parse(breadcrumb) : [];
    }

    // 娓呴櫎闈㈠寘灞?    clearBreadcrumb() {
        localStorage.removeItem(this.breadcrumbKey);
    }

    // 娓叉煋闈㈠寘灞?    renderBreadcrumb(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        const breadcrumb = this.getBreadcrumb();
        if (breadcrumb.length === 0) {
            container.innerHTML = '<span class="breadcrumb-item">棣栭〉</span>';
            return;
        }
        
        let html = '<a href="index.html" class="breadcrumb-item">棣栭〉</a>';
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

// 鍔犺浇鐘舵€佺鐞嗗櫒
class LoadingManager {
    constructor() {
        this.loadingElements = new Map();
    }

    // 鏄剧ず鍔犺浇鐘舵€?    showLoading(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.style.display = 'block';
            this.loadingElements.set(elementId, element);
        }
    }

    // 闅愯棌鍔犺浇鐘舵€?    hideLoading(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.style.display = 'none';
            this.loadingElements.delete(elementId);
        }
    }

    // 闅愯棌鎵€鏈夊姞杞界姸鎬?    hideAllLoading() {
        this.loadingElements.forEach((element, id) => {
            element.style.display = 'none';
        });
        this.loadingElements.clear();
    }
}

// 閫氱煡绠＄悊鍣?class NotificationManager {
    constructor() {
        this.containerId = 'notification-container';
        this.createContainer();
    }

    // 鍒涘缓閫氱煡瀹瑰櫒
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
            document.body.appendChild(container);
        }
    }

    // 鏄剧ず閫氱煡
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
        container.appendChild(notification);
        
        // 鑷姩鍏抽棴
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, duration);
    }

    // 鏄剧ず鎴愬姛閫氱煡
    success(message, duration = 3000) {
        this.show(message, 'success', duration);
    }

    // 鏄剧ず閿欒閫氱煡
    error(message, duration = 5000) {
        this.show(message, 'error', duration);
    }

    // 鏄剧ず璀﹀憡閫氱煡
    warning(message, duration = 4000) {
        this.show(message, 'warning', duration);
    }

    // 鏄剧ず淇℃伅閫氱煡
    info(message, duration = 3000) {
        this.show(message, 'info', duration);
    }
}

// 鍒濆鍖栨墍鏈夌鐞嗗櫒
const authManager = new AuthManager();
const pageStateManager = new PageStateManager();
const formManager = new FormManager();
const navigationManager = new NavigationManager();
const loadingManager = new LoadingManager();
const notificationManager = new NotificationManager();

// 椤甸潰杩囨浮鍔ㄧ敾
function addPageTransition() {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.3s ease-in-out';
    
    window.addEventListener('load', () => {
        document.body.style.opacity = '1';
    });
    
    // 涓烘墍鏈夐摼鎺ユ坊鍔犺繃娓℃晥鏋?    document.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', (e) => {
            // 鍙鐞嗗悓婧愰摼鎺?            if (link.hostname === window.location.hostname) {
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

// 娣诲姞CSS鍔ㄧ敾
function addAnimations() {
    const style = document.createElement('style');
    style.textContent = `
        /* 椤甸潰杩囨浮鍔ㄧ敾 */
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
        
        /* 鍔犺浇鍔ㄧ敾 */
        @keyframes spin {
            to {
                transform: rotate(360deg);
            }
        }
        
        /* 鎸夐挳鎮仠鍔ㄧ敾 */
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
        
        /* 闈㈠寘灞戞牱寮?*/
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
        
        /* 鐧诲綍鐘舵€佹寚绀哄櫒 */
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
        
        /* 鍝嶅簲寮忚璁?*/
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
        
        /* 鍔犺浇鐘舵€佷紭鍖?*/
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
        
        /* 鎸夐挳浜や簰鍙嶉 */
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
        
        /* 琛ㄥ崟鍏冪礌浜や簰 */
        input, textarea, select {
            transition: all 0.3s ease;
        }
        
        input:focus, textarea:focus, select:focus {
            outline: none;
            box-shadow: 0 0 10px rgba(0, 255, 157, 0.2);
            border-color: var(--color-primary);
        }
        
        /* 閫氱煡鏍峰紡 */
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

// 鍒濆鍖栭〉闈?function initPage(pageName, pageLabel) {
    // 娣诲姞椤甸潰杩囨浮鍔ㄧ敾
    addPageTransition();
    
    // 娣诲姞CSS鍔ㄧ敾
    addAnimations();
    
    // 娣诲姞闈㈠寘灞?    navigationManager.addBreadcrumbItem(pageLabel, window.location.pathname);
    
    // 娓叉煋闈㈠寘灞?    const breadcrumbContainer = document.getElementById('breadcrumb');
    if (breadcrumbContainer) {
        navigationManager.renderBreadcrumb('breadcrumb');
    }
    
    // 妫€鏌ョ櫥褰曠姸鎬?    if (authManager.isAuthenticated()) {
        // 鏇存柊token杩囨湡鏃堕棿
        authManager.updateExpiry();
        
        // 鏄剧ず鐧诲綍鐘舵€?        const authIndicator = document.getElementById('auth-indicator');
        if (authIndicator) {
            const user = authManager.getAuth().user;
            authIndicator.innerHTML = `
                <div class="auth-status"></div>
                <span>${user.username}</span>
            `;
        }
    } else {
        // 娓呴櫎杩囨湡鐨勭櫥褰曠姸鎬?        authManager.logout();
    }
    
    // 淇濆瓨椤甸潰鐘舵€?    window.addEventListener('beforeunload', () => {
        const state = {
            scrollY: window.scrollY,
            timestamp: Date.now()
        };
        pageStateManager.saveState(pageName, state);
    });
    
    // 鎭㈠椤甸潰鐘舵€?    window.addEventListener('load', () => {
        const savedState = pageStateManager.getState(pageName);
        if (savedState) {
            // 鍙仮澶嶆渶杩?鍒嗛挓鐨勭姸鎬?            if (Date.now() - savedState.timestamp < 5 * 60 * 1000) {
                window.scrollTo(0, savedState.state.scrollY);
            }
        }
    });
}

// 瀵煎嚭鍏ㄥ眬鍙橀噺
window.authManager = authManager;
window.pageStateManager = pageStateManager;
window.formManager = formManager;
window.navigationManager = navigationManager;
window.loadingManager = loadingManager;
window.notificationManager = notificationManager;
window.initPage = initPage;