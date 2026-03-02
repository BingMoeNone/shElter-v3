from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_create_user(client: TestClient):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "Test@123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert data["data"] is not None
    assert data["data"]["username"] == "testuser"
    assert data["data"]["email"] == "test@example.com"


def test_create_user_with_same_username(client: TestClient):
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test1@example.com",
            "password": "Test@123",
        },
    )
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test2@example.com",
            "password": "Test@123",
        },
    )
    assert response.status_code == 400
    data = response.json()
    assert data["status"] == 400
    assert data["error_code"] == "USERNAME_EXISTS"


def test_create_user_with_same_email(client: TestClient):
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "user1",
            "email": "same@example.com",
            "password": "Test@123",
        },
    )
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "user2",
            "email": "same@example.com",
            "password": "Test@123",
        },
    )
    assert response.status_code == 400
    data = response.json()
    assert data["status"] == 400
    assert data["error_code"] == "EMAIL_EXISTS"


def test_login(client: TestClient):
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "Test@123",
        },
    )
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "Test@123"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert data["data"] is not None
    assert "access_token" in data["data"]
    assert "refresh_token" in data["data"]
    assert data["data"]["user"]["username"] == "testuser"


def test_login_wrong_password(client: TestClient):
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "Test@123",
        },
    )
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "Wrong@123"
        },
    )
    assert response.status_code == 401
    data = response.json()
    assert data["status"] == 401
    assert data["error_code"] == "INVALID_CREDENTIALS"


def test_login_username_email_mismatch(client: TestClient):
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "user1",
            "email": "user1@example.com",
            "password": "Test@123",
        },
    )
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "user2",
            "email": "user2@example.com",
            "password": "Test@123",
        },
    )
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "user2",
            "email": "user1@example.com",
            "password": "Test@123"
        },
    )
    assert response.status_code == 401
    data = response.json()
    assert data["status"] == 401
    assert data["error_code"] == "INVALID_CREDENTIALS"


def test_login_nonexistent_email(client: TestClient):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "nonexistent",
            "email": "nonexistent@example.com",
            "password": "Test@123"
        },
    )
    assert response.status_code == 401
    data = response.json()
    assert data["status"] == 401
    assert data["error_code"] == "INVALID_CREDENTIALS"
