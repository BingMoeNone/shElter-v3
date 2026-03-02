from fastapi.testclient import TestClient


def test_get_health(client: TestClient):
    """测试健康检查端点"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_get_articles_unauthorized(client: TestClient):
    """测试未登录用户获取文章列表"""
    response = client.get("/api/v1/articles")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert isinstance(data["data"], list)


def test_register_and_login(client: TestClient):
    """测试用户注册和登录"""
    # 注册用户
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "Test@123",
        },
    )
    assert register_response.status_code == 200
    register_data = register_response.json()
    assert register_data["status"] == 200
    assert register_data["data"] is not None
    assert register_data["data"]["username"] == "testuser"
    assert register_data["data"]["email"] == "test@example.com"
    
    # 登录获取token
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "Test@123"
        },
    )
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert login_data["status"] == 200
    assert login_data["data"] is not None
    assert "access_token" in login_data["data"]
    assert "refresh_token" in login_data["data"]
    assert login_data["data"]["user"]["username"] == "testuser"
    
    return login_data["data"]["access_token"]


def test_create_article(client: TestClient):
    """测试创建文章"""
    # 先登录获取token
    token = test_register_and_login(client)
    
    # 创建文章
    article_data = {
        "title": "测试文章",
        "content": "这是一篇测试文章的内容",
        "summary": "这是一篇测试文章的摘要",
        "status": "draft"
    }
    
    response = client.post(
        "/api/v1/articles",
        json=article_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert data["data"] is not None
    assert data["data"]["title"] == article_data["title"]
    assert data["data"]["content"] == article_data["content"]
    assert data["data"]["summary"] == article_data["summary"]
    assert data["data"]["status"] == article_data["status"]


def test_get_article_by_id(client: TestClient):
    """测试根据ID获取文章"""
    # 先登录获取token并创建文章
    token = test_register_and_login(client)
    
    # 创建文章
    article_data = {
        "title": "测试文章",
        "content": "这是一篇测试文章的内容",
        "summary": "这是一篇测试文章的摘要",
        "status": "published"
    }
    
    create_response = client.post(
        "/api/v1/articles",
        json=article_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert create_response.status_code == 200
    create_data = create_response.json()
    article_id = create_data["data"]["id"]
    
    # 根据ID获取文章
    get_response = client.get(f"/api/v1/articles/{article_id}")
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert get_data["status"] == 200
    assert get_data["data"] is not None
    assert get_data["data"]["id"] == article_id
    assert get_data["data"]["title"] == article_data["title"]


def test_update_article(client: TestClient):
    """测试更新文章"""
    # 先登录获取token并创建文章
    token = test_register_and_login(client)
    
    # 创建文章
    article_data = {
        "title": "测试文章",
        "content": "这是一篇测试文章的内容",
        "summary": "这是一篇测试文章的摘要",
        "status": "draft"
    }
    
    create_response = client.post(
        "/api/v1/articles",
        json=article_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert create_response.status_code == 200
    create_data = create_response.json()
    article_id = create_data["data"]["id"]
    
    # 更新文章
    update_data = {
        "title": "更新后的测试文章",
        "content": "这是更新后的测试文章内容",
        "summary": "这是更新后的测试文章摘要",
        "status": "published"
    }
    
    update_response = client.put(
        f"/api/v1/articles/{article_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert update_response.status_code == 200
    update_result = update_response.json()
    assert update_result["status"] == 200
    assert update_result["data"] is not None
    assert update_result["data"]["title"] == update_data["title"]
    assert update_result["data"]["content"] == update_data["content"]
    assert update_result["data"]["status"] == update_data["status"]


def test_delete_article(client: TestClient):
    """测试删除文章"""
    # 先登录获取token并创建文章
    token = test_register_and_login(client)
    
    # 创建文章
    article_data = {
        "title": "测试文章",
        "content": "这是一篇测试文章的内容",
        "summary": "这是一篇测试文章的摘要",
        "status": "draft"
    }
    
    create_response = client.post(
        "/api/v1/articles",
        json=article_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert create_response.status_code == 200
    create_data = create_response.json()
    article_id = create_data["data"]["id"]
    
    # 删除文章
    delete_response = client.delete(
        f"/api/v1/articles/{article_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # 检查删除后的响应
    assert delete_response.status_code == 200
    delete_result = delete_response.json()
    assert delete_result["status"] == 200
    
    # 检查文章是否被删除
    get_response = client.get(f"/api/v1/articles/{article_id}")
    assert get_response.status_code == 404
