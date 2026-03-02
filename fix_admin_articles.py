import os
import re

def fix_admin_articles():
    filepath = r"c:\BM_Program\shElter-v3\frontend-legacy\admin-articles.html"

    content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文章管理</title>
    <style>
        :root {
            --color-primary: #00ff9d;
            --color-text: #fff;
            --color-text-muted: #aaa;
            --color-surface: #1a1a1a;
            --color-border: #333;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif, 'Microsoft YaHei', '微软雅黑', SimHei, '黑体', sans-serif;
            background-color: var(--color-background);
            color: var(--color-text);
            line-height: 1.6;
        }

        header {
            background: var(--color-surface);
            padding: 15px 20px;
            border-bottom: 1px solid var(--color-border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
        }

        nav ul {
            list-style: none;
            display: flex;
            gap: 20px;
        }

        nav a {
            color: var(--color-text);
            text-decoration: none;
            padding: 8px 15px;
            border-radius: 4px;
            transition: all 0.3s ease;
        }

        nav a:hover, nav a.active {
            background: var(--color-primary);
            color: #000;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .page-title {
            font-size: 2rem;
            color: var(--color-primary);
            margin-bottom: 20px;
            text-align: center;
        }

        .articles-header {
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .search-bar {
            flex: 1;
            min-width: 250px;
        }

        .search-bar input {
            width: 100%;
            padding: 10px;
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid var(--color-border);
            border-radius: 4px;
            color: var(--color-text);
            font-size: 1rem;
        }

        .search-bar input:focus {
            outline: none;
            border-color: var(--color-primary);
            box-shadow: 0 0 10px rgba(0, 255, 157, 0.2);
        }

        .filter-bar {
            min-width: 200px;
        }

        .filter-bar select {
            width: 100%;
            padding: 10px;
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid var(--color-border);
            border-radius: 4px;
            color: var(--color-text);
            font-size: 1rem;
        }

        .loading {
            text-align: center;
            font-size: 1.2rem;
            color: var(--color-text-muted);
            padding: 40px;
        }

        .articles-table-container {
            overflow-x: auto;
        }

        .articles-table {
            width: 100%;
            border-collapse: collapse;
            background: var(--color-surface);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 0 15px rgba(0, 255, 157, 0.1);
        }

        .articles-table th,
        .articles-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid var(--color-border);
        }

        .articles-table th {
            background: rgba(0, 255, 157, 0.1);
            color: var(--color-primary);
            font-weight: bold;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .articles-table tr:last-child td {
            border-bottom: none;
        }

        .articles-table tr:hover {
            background: rgba(0, 255, 157, 0.05);
        }

        .article-title {
            max-width: 300px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .article-title a {
            color: var(--color-primary);
            text-decoration: none;
        }

        .article-title a:hover {
            text-decoration: underline;
        }

        .status-badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: bold;
            text-transform: capitalize;
        }

        .status-published {
            background: rgba(67, 233, 123, 0.2);
            color: #43e97b;
        }

        .status-draft {
            background: rgba(255, 204, 0, 0.2);
            color: #ffcc00;
        }

        .status-archived {
            background: rgba(255, 107, 107, 0.2);
            color: #ff6b6b;
        }

        .action-buttons {
            display: flex;
            gap: 8px;
        }

        .btn {
            padding: 6px 12px;
            border: 1px solid var(--color-border);
            border-radius: 4px;
            font-size: 0.8rem;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }

        .btn-edit {
            background: rgba(0, 255, 157, 0.1);
            color: var(--color-primary);
        }

        .btn-edit:hover {
            background: var(--color-primary);
            color: #000;
        }

        .btn-delete {
            background: rgba(255, 107, 107, 0.1);
            color: #ff6b6b;
        }

        .btn-delete:hover {
            background: #ff6b6b;
            color: #fff;
        }

        .pagination {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 20px;
            gap: 10px;
        }

        .page-btn {
            padding: 8px 16px;
            background: rgba(0, 255, 157, 0.1);
            color: var(--color-primary);
            border: 1px solid var(--color-primary);
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .page-btn:hover:not(:disabled) {
            background: var(--color-primary);
            color: #000;
        }

        .page-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .page-info {
            font-size: 0.9rem;
            color: var(--color-text-muted);
        }
    </style>
</head>
<body>
    <header>
        <h1>管理后台</h1>
        <nav>
            <ul>
                <li><a href="admin-dashboard.html">仪表盘</a></li>
                <li><a href="admin-articles.html" class="active">文章管理</a></li>
                <li><a href="admin-users.html">用户管理</a></li>
                <li><a href="admin-comments.html">评论管理</a></li>
                <li><a href="admin-moderation.html">内容审核</a></li>
                <li><a href="index.html">返回首页</a></li>
            </ul>
        </nav>
    </header>

    <div class="container">
        <h1 class="page-title">文章管理</h1>
        
        <div class="articles-header">
            <div class="search-bar">
                <input
                    type="text"
                    id="searchQuery"
                    placeholder="搜索文章标题..."
                />
            </div>
            <div class="filter-bar">
                <select id="statusFilter">
                    <option value="">所有状态</option>
                    <option value="published">已发布</option>
                    <option value="draft">草稿</option>
                    <option value="archived">已归档</option>
                </select>
            </div>
        </div>
        
        <div id="loading" class="loading">加载中...</div>
        
        <div id="articlesTableContainer" class="articles-table-container" style="display: none;">
            <table class="articles-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>标题</th>
                        <th>作者</th>
                        <th>状态</th>
                        <th>浏览量</th>
                        <th>创建时间</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody id="articlesTableBody">
                </tbody>
            </table>
            
            <div id="pagination" class="pagination">
                <button 
                    class="page-btn" 
                    id="prevPageBtn"
                    disabled
                >
                    上一页
                </button>
                
                <span class="page-info" id="pageInfo">
                    第 1 / 1 页
                </span>
                
                <button 
                    class="page-btn" 
                    id="nextPageBtn"
                    disabled
                >
                    下一页
                </button>
            </div>
        </div>
    </div>

    <script>
        const mockArticles = [
            {
                id: 1,
                title: "FastAPI后端开发最佳实践",
                author: { username: "admin" },
                status: "published",
                view_count: 1234,
                created_at: "2023-01-15T10:30:00Z"
            },
            {
                id: 2,
                title: "Vue3组合式API使用指南",
                author: { username: "testuser" },
                status: "published",
                view_count: 890,
                created_at: "2023-02-20T14:20:00Z"
            },
            {
                id: 3,
                title: "Python异步编程入门",
                author: { username: "admin" },
                status: "draft",
                view_count: 456,
                created_at: "2023-03-10T09:15:00Z"
            },
            {
                id: 4,
                title: "TypeScript高级类型技巧",
                author: { username: "moderator" },
                status: "published",
                view_count: 789,
                created_at: "2023-04-05T16:45:00Z"
            },
            {
                id: 5,
                title: "Docker容器化部署教程",
                author: { username: "admin" },
                status: "archived",
                view_count: 234,
                created_at: "2023-05-12T11:30:00Z"
            }
        ];

        let articles = [];
        let loading = true;
        let searchQuery = '';
        let currentPage = 1;
        let limit = 20;
        let totalItems = 0;
        let totalPages = 0;
        let statusFilter = '';

        document.addEventListener('DOMContentLoaded', function() {
            bindEventListeners();
            fetchArticles();
        });

        function bindEventListeners() {
            const searchInput = document.getElementById('searchQuery');
            const statusFilterSelect = document.getElementById('statusFilter');
            const prevPageBtn = document.getElementById('prevPageBtn');
            const nextPageBtn = document.getElementById('nextPageBtn');

            searchInput.addEventListener('input', function() {
                searchQuery = this.value;
                currentPage = 1;
                fetchArticles();
            });

            statusFilterSelect.addEventListener('change', function() {
                statusFilter = this.value;
                currentPage = 1;
                fetchArticles();
            });

            prevPageBtn.addEventListener('click', function() {
                handlePageChange(currentPage - 1);
            });

            nextPageBtn.addEventListener('click', function() {
                handlePageChange(currentPage + 1);
            });
        }

        function fetchArticles() {
            loading = true;
            updateUI();
            
            setTimeout(() => {
                try {
                    let filteredArticles = [...mockArticles];
                    
                    if (searchQuery) {
                        filteredArticles = filteredArticles.filter(article => 
                            article.title.toLowerCase().includes(searchQuery.toLowerCase())
                        );
                    }
                    
                    if (statusFilter) {
                        filteredArticles = filteredArticles.filter(article => 
                            article.status === statusFilter
                        );
                    }
                    
                    articles = filteredArticles;
                    totalItems = articles.length;
                    totalPages = Math.ceil(totalItems / limit);
                } catch (error) {
                    console.error('Failed to fetch articles:', error);
                } finally {
                    loading = false;
                    updateUI();
                }
            }, 500);
        }

        function updateUI() {
            const loadingElement = document.getElementById('loading');
            const articlesTableContainer = document.getElementById('articlesTableContainer');
            
            if (loading) {
                loadingElement.style.display = 'block';
                articlesTableContainer.style.display = 'none';
            } else {
                loadingElement.style.display = 'none';
                articlesTableContainer.style.display = 'block';
                renderArticlesTable();
                updatePagination();
            }
        }

        function renderArticlesTable() {
            const tableBody = document.getElementById('articlesTableBody');
            tableBody.innerHTML = '';
            
            const startIndex = (currentPage - 1) * limit;
            const endIndex = startIndex + limit;
            const currentArticles = articles.slice(startIndex, endIndex);
            
            currentArticles.forEach(article => {
                const row = document.createElement('tr');
                
                const createdAt = new Date(article.created_at).toLocaleString();
                const statusClass = `status-${article.status}`;
                const statusText = {
                    'published': '已发布',
                    'draft': '草稿',
                    'archived': '已归档'
                }[article.status] || article.status;
                
                row.innerHTML = `
                    <td>${article.id}</td>
                    <td class="article-title">
                        <a href="article-detail.html?id=${article.id}">${article.title}</a>
                    </td>
                    <td>${article.author.username}</td>
                    <td>
                        <span class="status-badge ${statusClass}">
                            ${statusText}
                        </span>
                    </td>
                    <td>${article.view_count}</td>
                    <td>${createdAt}</td>
                    <td>
                        <div class="action-buttons">
                            <a href="edit-article.html?id=${article.id}" class="btn btn-edit">编辑</a>
                            <button class="btn btn-delete" onclick="handleDeleteArticle(${article.id})">删除</button>
                        </div>
                    </td>
                `;
                
                tableBody.appendChild(row);
            });
        }

        function updatePagination() {
            const prevPageBtn = document.getElementById('prevPageBtn');
            const nextPageBtn = document.getElementById('nextPageBtn');
            const pageInfo = document.getElementById('pageInfo');
            
            pageInfo.textContent = `第 ${currentPage} / ${totalPages} 页`;
            prevPageBtn.disabled = currentPage === 1;
            nextPageBtn.disabled = currentPage === totalPages;
        }

        function handlePageChange(page) {
            if (page < 1 || page > totalPages) return;
            currentPage = page;
            fetchArticles();
        }

        function handleDeleteArticle(articleId) {
            if (confirm('确定要删除这篇文章吗？')) {
                setTimeout(() => {
                    mockArticles = mockArticles.filter(article => article.id !== articleId);
                    fetchArticles();
                }, 300);
            }
        }
    </script>
</body>
</html>"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed: {filepath}")

if __name__ == "__main__":
    fix_admin_articles()
