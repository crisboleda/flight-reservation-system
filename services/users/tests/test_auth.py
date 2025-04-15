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
