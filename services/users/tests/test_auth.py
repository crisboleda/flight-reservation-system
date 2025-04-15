def test_register_user(client):
    response = client.post(
        "/api/users/register",
        json={
            "name": "Example",
            "email": "testuser@gmail.com",
            "password": "secret123",
        },
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@gmail.com"
    assert "id" in data


def test_login_user(client):
    client.post(
        "/api/users/register",
        json={
            "name": "Example",
            "email": "testuser@gmail.com",
            "password": "secret123",
        },
        headers={"Content-Type": "application/json"},
    )

    response = client.post(
        "/api/users/login",
        json={"email": "testuser@gmail.com", "password": "secret123"},
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_verify_token(client):
    client.post(
        "/api/users/register",
        json={
            "name": "Example",
            "email": "testuser@gmail.com",
            "password": "secret123",
        },
        headers={"Content-Type": "application/json"},
    )

    response_login = client.post(
        "/api/users/login",
        json={"email": "testuser@gmail.com", "password": "secret123"},
        headers={"Content-Type": "application/json"},
    )
    data = response_login.json()
    access_token = data["access_token"]

    response_verify_token = client.post(
        "/api/users/verify-token",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response_verify_token.status_code == 200


def test_token_unauthorized(client):
    response_verify_token = client.post(
        "/api/users/verify-token",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer invalid.token",
        },
    )
    assert response_verify_token.status_code == 401
