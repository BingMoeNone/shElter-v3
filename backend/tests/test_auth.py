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


def test_create_user_with_same_username(client: TestClient):
    client.post(
        "/api/v1/users/",
        json={
            "username": "testuser",
            "email": "test1@example.com",
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
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test2@example.com"


def test_create_user_with_same_email(client: TestClient):
    client.post(
        "/api/v1/users/",
        json={
            "username": "user1",
            "email": "same@example.com",
            "password": "TestPassword123",
        },
    )
    response = client.post(
        "/api/v1/users/",
        json={
            "username": "user2",
            "email": "same@example.com",
            "password": "TestPassword123",
        },
    )
    assert response.status_code == 409
    data = response.json()
    assert data["detail"]["code"] == "EMAIL_ALREADY_REGISTERED"


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
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["username"] == "testuser"


def test_login_wrong_password(client: TestClient):
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
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "WrongPassword123"
        },
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"]["code"] == "INVALID_CREDENTIALS"


def test_login_username_email_mismatch(client: TestClient):
    client.post(
        "/api/v1/users/",
        json={
            "username": "user1",
            "email": "user1@example.com",
            "password": "TestPassword123",
        },
    )
    client.post(
        "/api/v1/users/",
        json={
            "username": "user2",
            "email": "user2@example.com",
            "password": "TestPassword123",
        },
    )
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "user2",
            "email": "user1@example.com",
            "password": "TestPassword123"
        },
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"]["code"] == "USERNAME_EMAIL_MISMATCH"


def test_login_nonexistent_email(client: TestClient):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "nonexistent",
            "email": "nonexistent@example.com",
            "password": "TestPassword123"
        },
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"]["code"] == "INVALID_CREDENTIALS"
