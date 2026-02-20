from fastapi.testclient import TestClient


def test_create_article(client: TestClient):
    user_response = client.post(
        "/api/v1/users/",
        json={
            "username": "author",
            "email": "author@example.com",
            "password": "TestPassword123",
        },
    )
    assert user_response.status_code == 201
    
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "author",
            "email": "author@example.com",
            "password": "TestPassword123"
        },
    )
    token = login_response.json()["access_token"]
    
    response = client.post(
        "/api/v1/articles/",
        json={
            "title": "Test Article",
            "content": "This is the content of the test article.",
            "summary": "A test article summary",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Article"
    assert data["status"] == "draft"


def test_list_articles(client: TestClient):
    user_response = client.post(
        "/api/v1/users/",
        json={
            "username": "author2",
            "email": "author2@example.com",
            "password": "TestPassword123",
        },
    )
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "author2",
            "email": "author2@example.com",
            "password": "TestPassword123"
        },
    )
    token = login_response.json()["access_token"]
    
    client.post(
        "/api/v1/articles/",
        json={
            "title": "Published Article",
            "content": "Content of published article.",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    
    response = client.get("/api/v1/articles/")
    assert response.status_code == 200
    data = response.json()
    assert "articles" in data
    assert "pagination" in data


def test_publish_article(client: TestClient):
    user_response = client.post(
        "/api/v1/users/",
        json={
            "username": "publisher",
            "email": "publisher@example.com",
            "password": "TestPassword123",
        },
    )
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "publisher",
            "email": "publisher@example.com",
            "password": "TestPassword123"
        },
    )
    token = login_response.json()["access_token"]
    
    create_response = client.post(
        "/api/v1/articles/",
        json={
            "title": "Article to Publish",
            "content": "This article will be published.",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    article_id = create_response.json()["id"]
    
    response = client.post(
        f"/api/v1/articles/{article_id}/publish",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "published"
    assert data["published_at"] is not None
