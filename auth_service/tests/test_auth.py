async def test_register_success(client):
    """Тест регистрации из урока 2 (Интеграционный)"""
    response = await client.post(
        "/auth/register",
        json={"email": "student@mephi.ru", "password": "password123"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "student@mephi.ru"

async def test_login_success(client):
    """Тест логина через OAuth2 форму"""
    await client.post(
        "/auth/register",
        json={"email": "test@test.ru", "password": "safe_password"}
    )

    response = await client.post(
        "/auth/login",
        data={"username": "test@test.ru", "password": "safe_password"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

async def test_get_me_unauthorized(client):
    """Проверка ошибки 401 (из урока 2)"""
    response = await client.get("/auth/me")
    assert response.status_code == 401