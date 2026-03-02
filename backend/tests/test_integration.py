from fastapi.testclient import TestClient


def test_full_user_flow(client: TestClient):
    """测试完整的用户流程：注册、登录、创建文章、获取文章、添加评论"""
    
    # 1. 注册新用户
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "integrationtest",
            "email": "integration@example.com",
            "password": "Test@123",
        },
    )
    assert register_response.status_code == 200
    register_data = register_response.json()
    assert register_data["status"] == 200
    assert register_data["data"] is not None
    
    # 2. 用户登录
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "integrationtest",
            "email": "integration@example.com",
            "password": "Test@123"
        },
    )
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert login_data["status"] == 200
    assert login_data["data"] is not None
    assert "access_token" in login_data["data"]
    access_token = login_data["data"]["access_token"]
    
    # 3. 创建新文章
    article_response = client.post(
        "/api/v1/articles",
        json={
            "title": "Integration Test Article",
            "content": "This is a test article for integration testing.",
            "summary": "Integration test article summary",
            "status": "published"
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert article_response.status_code == 200
    article_data = article_response.json()
    assert article_data["status"] == 200
    assert article_data["data"] is not None
    article_id = article_data["data"]["id"]
    
    # 4. 获取文章列表，确认新文章存在
    articles_response = client.get("/api/v1/articles")
    assert articles_response.status_code == 200
    articles_data = articles_response.json()
    assert articles_data["status"] == 200
    assert isinstance(articles_data["data"], list)
    assert any(article["id"] == article_id for article in articles_data["data"])
    
    # 5. 获取单个文章详情
    single_article_response = client.get(f"/api/v1/articles/{article_id}")
    assert single_article_response.status_code == 200
    single_article_data = single_article_response.json()
    assert single_article_data["status"] == 200
    assert single_article_data["data"] is not None
    assert single_article_data["data"]["id"] == article_id
    assert single_article_data["data"]["title"] == "Integration Test Article"
    
    # 6. 添加评论到文章
    comment_response = client.post(
        "/api/v1/comments",
        json={
            "articleId": article_id,
            "content": "This is a test comment for the integration test article."
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert comment_response.status_code == 200
    comment_data = comment_response.json()
    assert comment_data["status"] == 200
    assert comment_data["data"] is not None
    comment_id = comment_data["data"]["id"]
    
    # 7. 获取文章的评论列表
    comments_response = client.get(f"/api/v1/articles/{article_id}/comments")
    assert comments_response.status_code == 200
    comments_data = comments_response.json()
    assert comments_data["status"] == 200
    assert isinstance(comments_data["data"], list)
    assert any(comment["id"] == comment_id for comment in comments_data["data"])
    
    # 8. 更新文章
    update_response = client.put(
        f"/api/v1/articles/{article_id}",
        json={
            "title": "Updated Integration Test Article",
            "content": "This is an updated test article for integration testing.",
            "summary": "Updated integration test article summary",
            "status": "published"
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert update_response.status_code == 200
    update_data = update_response.json()
    assert update_data["status"] == 200
    assert update_data["data"] is not None
    assert update_data["data"]["title"] == "Updated Integration Test Article"
    
    # 9. 删除评论
    delete_comment_response = client.delete(
        f"/api/v1/comments/{comment_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert delete_comment_response.status_code == 200
    delete_comment_data = delete_comment_response.json()
    assert delete_comment_data["status"] == 200
    
    # 10. 删除文章
    delete_article_response = client.delete(
        f"/api/v1/articles/{article_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert delete_article_response.status_code == 200
    delete_article_data = delete_article_response.json()
    assert delete_article_data["status"] == 200
    
    # 11. 确认文章已删除
    get_deleted_article_response = client.get(f"/api/v1/articles/{article_id}")
    assert get_deleted_article_response.status_code == 404
    
    print("✅ 完整集成测试流程通过！")


def test_article_crud_flow(client: TestClient):
    """测试文章的CRUD流程"""
    
    # 注册并登录用户
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "crudtest",
            "email": "crud@example.com",
            "password": "Test@123",
        },
    )
    assert register_response.status_code == 200
    
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "crudtest",
            "email": "crud@example.com",
            "password": "Test@123"
        },
    )
    assert login_response.status_code == 200
    access_token = login_response.json()["data"]["access_token"]
    
    # 创建多篇文章用于测试
    article_ids = []
    for i in range(3):
        article_response = client.post(
            "/api/v1/articles",
            json={
                "title": f"CRUD Test Article {i+1}",
                "content": f"This is CRUD test article {i+1} content.",
                "summary": f"CRUD test article {i+1} summary",
                "status": "published"
            },
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert article_response.status_code == 200
        article_ids.append(article_response.json()["data"]["id"])
    
    # 获取所有文章并验证数量
    articles_response = client.get("/api/v1/articles")
    assert articles_response.status_code == 200
    articles_data = articles_response.json()
    assert len(articles_data["data"]) >= 3
    
    # 测试文章排序功能
    sorted_articles_response = client.get("/api/v1/articles?sort_by=created_at&sort_order=desc")
    assert sorted_articles_response.status_code == 200
    sorted_articles_data = sorted_articles_response.json()
    assert len(sorted_articles_data["data"]) >= 3
    
    # 测试文章过滤功能
    filtered_articles_response = client.get(f"/api/v1/articles?author=crudtest")
    assert filtered_articles_response.status_code == 200
    filtered_articles_data = filtered_articles_response.json()
    assert len(filtered_articles_data["data"]) >= 3
    
    # 清理：删除所有创建的文章
    for article_id in article_ids:
        delete_response = client.delete(
            f"/api/v1/articles/{article_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert delete_response.status_code == 200
    
    print("✅ 文章CRUD流程测试通过！")


def test_comment_flow(client: TestClient):
    """测试评论的创建、获取和删除流程"""
    
    # 注册并登录用户
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "commenttest",
            "email": "comment@example.com",
            "password": "Test@123",
        },
    )
    assert register_response.status_code == 200
    
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "commenttest",
            "email": "comment@example.com",
            "password": "Test@123"
        },
    )
    assert login_response.status_code == 200
    access_token = login_response.json()["data"]["access_token"]
    
    # 创建测试文章
    article_response = client.post(
        "/api/v1/articles",
        json={
            "title": "Comment Test Article",
            "content": "This article is for testing comments.",
            "summary": "Comment test article",
            "status": "published"
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert article_response.status_code == 200
    article_id = article_response.json()["data"]["id"]
    
    # 创建多条评论
    comment_ids = []
    for i in range(5):
        comment_response = client.post(
            "/api/v1/comments",
            json={
                "articleId": article_id,
                "content": f"This is test comment {i+1}"
            },
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert comment_response.status_code == 200
        comment_ids.append(comment_response.json()["data"]["id"])
    
    # 获取文章的评论
    get_comments_response = client.get(f"/api/v1/articles/{article_id}/comments")
    assert get_comments_response.status_code == 200
    comments_data = get_comments_response.json()
    assert len(comments_data["data"]) == 5
    
    # 分页测试
    paginated_comments_response = client.get(f"/api/v1/articles/{article_id}/comments?page=1&limit=2")
    assert paginated_comments_response.status_code == 200
    paginated_comments_data = paginated_comments_response.json()
    assert len(paginated_comments_data["data"]) == 2
    
    # 清理：删除所有评论和文章
    for comment_id in comment_ids:
        delete_comment_response = client.delete(
            f"/api/v1/comments/{comment_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert delete_comment_response.status_code == 200
    
    delete_article_response = client.delete(
        f"/api/v1/articles/{article_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert delete_article_response.status_code == 200
    
    print("✅ 评论流程测试通过！")


def test_user_profile_flow(client: TestClient):
    """测试用户个人资料相关功能"""
    
    # 注册并登录用户
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "profiletest",
            "email": "profile@example.com",
            "password": "Test@123",
        },
    )
    assert register_response.status_code == 200
    
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "profiletest",
            "email": "profile@example.com",
            "password": "Test@123"
        },
    )
    assert login_response.status_code == 200
    access_token = login_response.json()["data"]["access_token"]
    
    # 获取当前用户信息
    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert me_response.status_code == 200
    me_data = me_response.json()
    assert me_data["status"] == 200
    assert me_data["data"]["username"] == "profiletest"
    
    # 更新用户信息
    update_response = client.put(
        "/api/v1/users/me",
        json={
            "display_name": "Profile Tester",
            "bio": "This is a test bio for the user profile."
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert update_response.status_code == 200
    update_data = update_response.json()
    assert update_data["status"] == 200
    assert update_data["data"]["display_name"] == "Profile Tester"
    assert update_data["data"]["bio"] == "This is a test bio for the user profile."
    
    # 获取用户公共资料
    profile_response = client.get("/api/v1/users/profiletest")
    assert profile_response.status_code == 200
    profile_data = profile_response.json()
    assert profile_data["status"] == 200
    assert profile_data["data"]["username"] == "profiletest"
    assert profile_data["data"]["display_name"] == "Profile Tester"
    
    print("✅ 用户资料流程测试通过！")
