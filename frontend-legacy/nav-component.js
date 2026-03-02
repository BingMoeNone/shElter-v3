/**
 * Navigation Component
 * Shared navigation with user menu for all pages
 */

// Navigation HTML template
const NAV_TEMPLATE = `
<nav class="main-nav">
    <div class="nav-container">
        <a href="index.html" class="nav-logo">Wiki Platform</a>
        <div class="nav-links">
            <a href="index.html" class="nav-link">首页</a>
            <a href="articles.html" class="nav-link">文章</a>
            <a href="categories.html" class="nav-link">分类</a>
            <a href="search.html" class="nav-link">搜索</a>
        </div>
        <div id="user-auth-section" class="nav-actions">
            <!-- 登录/注册按钮 -->
            <div id="auth-buttons">
                <a href="login.html" class="btn btn-outline">登录</a>
                <a href="register.html" class="btn">注册</a>
            </div>
            <!-- 用户信息显示 -->
            <div id="user-info" style="display: none;">
                <div class="user-profile">
                    <img id="user-avatar" src="" alt="用户头像" class="avatar">
                    <span id="user-name" class="username"></span>
                    <div class="user-menu">
                        <!-- 用户头部信息 -->
                        <div class="user-menu-header">
                            <img id="menu-user-avatar" src="" alt="用户头像" class="avatar">
                            <div class="user-info-text">
                                <span id="menu-user-name" class="user-name"></span>
                                <span id="menu-user-role" class="user-role">普通用户</span>
                            </div>
                        </div>
                        
                        <!-- 用户统计 -->
                        <div class="user-stats">
                            <div class="user-stat-item">
                                <span id="user-articles-count" class="user-stat-value">0</span>
                                <span class="user-stat-label">文章</span>
                            </div>
                            <div class="user-stat-item">
                                <span id="user-comments-count" class="user-stat-value">0</span>
                                <span class="user-stat-label">评论</span>
                            </div>
                            <div class="user-stat-item">
                                <span id="user-likes-count" class="user-stat-value">0</span>
                                <span class="user-stat-label">获赞</span>
                            </div>
                        </div>
                        
                        <!-- 个人中心 -->
                        <div class="menu-section">
                            <div class="menu-section-title">个人中心</div>
                            <a href="profile.html"><span class="icon">👤</span>个人资料</a>
                            <a href="edit-article.html"><span class="icon">✏️</span>写文章</a>
                            <a href="my-articles.html"><span class="icon">📝</span>我的文章</a>
                        </div>
                        
                        <!-- 账号设置 -->
                        <div class="menu-section">
                            <div class="menu-section-title">账号设置</div>
                            <a href="settings.html"><span class="icon">⚙️</span>设置</a>
                            <a href="#" id="logout-btn" class="logout"><span class="icon">🚪</span>退出登录</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</nav>
`;

// Navigation styles
const NAV_STYLES = `
<style>
    /* Main Navigation */
    .main-nav {
        background-color: var(--color-surface, #1a1a1a);
        padding: 1rem 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid var(--color-border, #333333);
        position: sticky;
        top: 0;
        z-index: 100;
    }

    .nav-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .nav-logo {
        font-size: 1.5rem;
        font-weight: bold;
        color: var(--color-primary, #0D8ABC);
        text-decoration: none;
    }

    .nav-links {
        display: flex;
        gap: 2rem;
    }

    .nav-link {
        color: var(--color-text, #ffffff);
        text-decoration: none;
        transition: color 0.3s ease;
        font-weight: 500;
    }

    .nav-link:hover {
        color: var(--color-primary, #0D8ABC);
    }

    .nav-actions {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    /* Buttons */
    .btn {
        display: inline-block;
        padding: 8px 16px;
        background: linear-gradient(135deg, var(--color-primary, #0D8ABC), var(--color-secondary, #9b59b6));
        color: white;
        text-decoration: none;
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        font-size: 0.9rem;
    }

    .btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(13, 138, 188, 0.3);
    }

    .btn-outline {
        background: transparent;
        border: 1px solid var(--color-primary, #0D8ABC);
        color: var(--color-primary, #0D8ABC);
    }

    .btn-outline:hover {
        background: var(--color-primary, #0D8ABC);
        color: white;
    }

    /* User Profile */
    .user-profile {
        display: flex;
        align-items: center;
        position: relative;
        cursor: pointer;
        padding: 4px 8px;
        border-radius: 8px;
        transition: background-color 0.2s ease;
    }

    .user-profile:hover {
        background-color: rgba(255, 255, 255, 0.05);
    }

    .avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        margin-right: 10px;
        border: 2px solid var(--color-primary, #0D8ABC);
        object-fit: cover;
    }

    .username {
        color: var(--color-text, #ffffff);
        font-weight: 500;
        font-size: 0.95rem;
    }

    /* User Menu */
    .user-menu {
        position: absolute;
        top: 100%;
        right: 0;
        margin-top: 12px;
        background-color: var(--color-surface, #1a1a1a);
        border: 1px solid var(--color-border, #333333);
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        min-width: 240px;
        padding: 12px 0;
        display: none;
        z-index: 1000;
    }

    .user-profile:hover .user-menu {
        display: block;
    }

    /* User Menu Header */
    .user-menu-header {
        padding: 16px;
        border-bottom: 1px solid var(--color-border, #333333);
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .user-menu-header .avatar {
        width: 52px;
        height: 52px;
        margin: 0;
    }

    .user-menu-header .user-info-text {
        flex: 1;
    }

    .user-menu-header .user-name {
        display: block;
        font-weight: 600;
        color: var(--color-text, #ffffff);
        margin-bottom: 4px;
        font-size: 1rem;
    }

    .user-menu-header .user-role {
        font-size: 0.85rem;
        color: var(--color-primary, #0D8ABC);
        background: rgba(13, 138, 188, 0.1);
        padding: 2px 8px;
        border-radius: 4px;
    }

    /* User Stats */
    .user-stats {
        display: flex;
        justify-content: space-around;
        padding: 16px;
        border-bottom: 1px solid var(--color-border, #333333);
    }

    .user-stat-item {
        text-align: center;
    }

    .user-stat-value {
        display: block;
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--color-primary, #0D8ABC);
    }

    .user-stat-label {
        font-size: 0.75rem;
        color: var(--color-text-muted, #a0a0a0);
        margin-top: 2px;
    }

    /* Menu Sections */
    .menu-section {
        padding: 8px 0;
    }

    .menu-section:not(:last-child) {
        border-bottom: 1px solid var(--color-border, #333333);
    }

    .menu-section-title {
        padding: 8px 16px;
        font-size: 0.7rem;
        color: var(--color-text-muted, #a0a0a0);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }

    .user-menu a {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 16px;
        color: var(--color-text, #ffffff);
        text-decoration: none;
        transition: all 0.2s ease;
        font-size: 0.95rem;
    }

    .user-menu a:hover {
        background-color: rgba(13, 138, 188, 0.1);
        color: var(--color-primary, #0D8ABC);
    }

    .user-menu a .icon {
        font-size: 1.2rem;
        width: 24px;
        text-align: center;
    }

    .user-menu a.logout {
        color: var(--color-danger, #e74c3c);
    }

    .user-menu a.logout:hover {
        background-color: rgba(231, 76, 60, 0.1);
    }

    /* Responsive */
    @media (max-width: 768px) {
        .nav-links {
            display: none;
        }
        
        .nav-container {
            padding: 0 16px;
        }
    }
</style>
`;

// Initialize navigation
function initNavigation() {
    // Insert styles
    document.head.insertAdjacentHTML('beforeend', NAV_STYLES);
    
    // Find existing nav and replace it, or insert at body start
    const existingNav = document.querySelector('nav');
    if (existingNav) {
        existingNav.outerHTML = NAV_TEMPLATE;
    } else {
        document.body.insertAdjacentHTML('afterbegin', NAV_TEMPLATE);
    }
    
    // Initialize user menu
    initUserMenu();
}

// Initialize user menu functionality
function initUserMenu() {
    // Check login status
    if (typeof authManager !== 'undefined' && authManager.isAuthenticated()) {
        showUserInfo();
    } else {
        showAuthButtons();
    }
}

// Show user info
function showUserInfo() {
    const auth = authManager.getAuth();
    const user = auth.user;
    
    // Hide auth buttons
    const authButtons = document.getElementById('auth-buttons');
    if (authButtons) authButtons.style.display = 'none';
    
    // Show user info
    const userInfo = document.getElementById('user-info');
    if (userInfo) userInfo.style.display = 'block';
    
    // Update user info
    const avatarUrl = user.avatar || 'https://ui-avatars.com/api/?name=' + encodeURIComponent(user.username) + '&background=0D8ABC&color=fff';
    
    const userAvatar = document.getElementById('user-avatar');
    if (userAvatar) userAvatar.src = avatarUrl;
    
    const userName = document.getElementById('user-name');
    if (userName) userName.textContent = user.username;
    
    // Update menu header
    const menuAvatar = document.getElementById('menu-user-avatar');
    if (menuAvatar) menuAvatar.src = avatarUrl;
    
    const menuUserName = document.getElementById('menu-user-name');
    if (menuUserName) menuUserName.textContent = user.username;
    
    const menuUserRole = document.getElementById('menu-user-role');
    if (menuUserRole) {
        menuUserRole.textContent = user.role === 'admin' ? '管理员' : (user.role === 'moderator' ? '版主' : '普通用户');
    }
    
    // Load user stats
    loadUserStats(user.id);
    
    // Add logout event
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            logout();
        });
    }
}

// Show auth buttons
function showAuthButtons() {
    const userInfo = document.getElementById('user-info');
    if (userInfo) userInfo.style.display = 'none';
    
    const authButtons = document.getElementById('auth-buttons');
    if (authButtons) authButtons.style.display = 'flex';
}

// Load user stats
async function loadUserStats(userId) {
    try {
        // Get stats from localStorage
        const stats = JSON.parse(localStorage.getItem('user_stats') || '{}');
        
        // Update display
        updateStatsDisplay(stats);
        
        // Try to fetch from API
        if (typeof authManager !== 'undefined') {
            const token = authManager.getToken();
            if (token) {
                const response = await fetch(`http://127.0.0.1:8000/api/v1/users/stats/${userId}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                
                if (response.ok) {
                    const data = await response.json();
                    if (data.data) {
                        const newStats = {
                            articles: data.data.total_articles || 0,
                            comments: data.data.total_comments || 0,
                            likes: data.data.total_likes || 0
                        };
                        
                        updateStatsDisplay(newStats);
                        localStorage.setItem('user_stats', JSON.stringify(newStats));
                    }
                }
            }
        }
    } catch (error) {
        console.log('Failed to load user stats:', error);
    }
}

// Update stats display
function updateStatsDisplay(stats) {
    const articlesCount = document.getElementById('user-articles-count');
    const commentsCount = document.getElementById('user-comments-count');
    const likesCount = document.getElementById('user-likes-count');
    
    if (articlesCount) articlesCount.textContent = stats.articles || 0;
    if (commentsCount) commentsCount.textContent = stats.comments || 0;
    if (likesCount) likesCount.textContent = stats.likes || 0;
}

// Logout function
function logout() {
    if (typeof authManager !== 'undefined') {
        authManager.logout();
    } else {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        localStorage.removeItem('expiry');
    }
    
    showAuthButtons();
    
    // Show notification
    if (typeof notificationManager !== 'undefined') {
        notificationManager.success('退出登录成功');
    }
    
    // Redirect to home after short delay
    setTimeout(() => {
        window.location.href = 'index.html';
    }, 1000);
}

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initNavigation);
} else {
    initNavigation();
}

// Export for manual use
window.NavigationComponent = {
    init: initNavigation,
    refresh: initUserMenu
};
