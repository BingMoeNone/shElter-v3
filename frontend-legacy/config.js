/**
 * 前端配置文件
 * 集中管理所有 API 地址和配置参数
 */

const CONFIG = {
    // API 基础配置
    API: {
        // 后端 API 基础 URL
        BASE_URL: 'http://127.0.0.1:8000/api/v1',
        // 超时时间（毫秒）
        TIMEOUT: 10000,
        // 重试次数
        RETRY_COUNT: 3,
        // 重试延迟（毫秒）
        RETRY_DELAY: 1000,
        // 速率限制配置
        RATE_LIMIT: {
            // 登录接口
            LOGIN: '10/minute',
            // 注册接口
            REGISTER: '5/minute',
            // 评论接口
            COMMENT: '20/minute',
            // 通用接口
            DEFAULT: '100/minute'
        }
    },
    
    // 前端运行配置
    FRONTEND: {
        // 开发服务器端口
        DEV_PORT: 5500,
        // 生产环境基础 URL
        PROD_BASE_URL: '',
        // 是否启用 mock 数据
        USE_MOCK: false,
        // Mock 数据延迟（毫秒）
        MOCK_DELAY: 800
    },
    
    // 功能开关
    FEATURES: {
        // 是否启用真实 API（false 时使用 mock 数据）
        USE_REAL_API: true,
        // 是否启用调试模式
        DEBUG_MODE: true,
        // 是否启用日志记录
        ENABLE_LOGGING: true,
        // 是否启用错误报告
        ENABLE_ERROR_REPORTING: true,
        // 是否启用性能监控
        ENABLE_PERFORMANCE_MONITORING: false
    },
    
    // 本地存储键名
    STORAGE_KEYS: {
        TOKEN: 'token',
        USER: 'user',
        EXPIRY: 'expiry',
        THEME: 'theme',
        LANGUAGE: 'language',
        PREFERENCES: 'preferences'
    },
    
    // 分页配置
    PAGINATION: {
        DEFAULT_PAGE_SIZE: 10,
        MAX_PAGE_SIZE: 100,
        PAGE_SIZE_OPTIONS: [10, 20, 50, 100]
    },
    
    // 错误处理配置
    ERROR_HANDLING: {
        // 自动重试的错误状态码
        RETRY_STATUS_CODES: [408, 429, 500, 502, 503, 504],
        // 需要重新认证的状态码
        AUTH_ERROR_CODES: [401, 403],
        // 错误提示显示时间（毫秒）
        ERROR_MESSAGE_DURATION: 5000,
        // 成功提示显示时间（毫秒）
        SUCCESS_MESSAGE_DURATION: 3000
    },
    
    // 缓存配置
    CACHE: {
        // 是否启用缓存
        ENABLE_CACHE: true,
        // 默认缓存时间（毫秒）
        DEFAULT_TTL: 5 * 60 * 1000, // 5 分钟
        // 文章列表缓存时间
        ARTICLES_TTL: 10 * 60 * 1000,
        // 用户信息缓存时间
        USER_TTL: 30 * 60 * 1000
    }
};

// 导出配置对象
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}
