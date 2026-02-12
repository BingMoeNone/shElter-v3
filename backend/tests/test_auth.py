from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_create_user(client: TestClient):
    response = client.post(
        "/api/v1/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


def test_create_duplicate_user(client: TestClient):
    client.post(
        "/api/v1/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123",
        },
    )
    response = client.post(
        "/api/v1/users/",
        json={
            "username": "testuser",
            "email": "test2@example.com",
            "password": "TestPassword123",
        },
    )
    assert response.status_code == 409


def test_login(client: TestClient):
    client.post(
        "/api/v1/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123",
        },
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "testuser", "password": "TestPassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["username"] == "testuser"


def test_login_invalid_credentials(client: TestClient):
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "nonexistent", "password": "wrongpassword"},
    )
    assert response.status_code == 401
