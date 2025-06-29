import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('email, password, username, status_code', [
    ('pytest1@pytest.com', 'test1234', 'pytest1', 201),  # зарегистрировался
    ('pytest1@pytest.com', 'test1234', 'pytest1', 400),  # отказ, уже зарегистрировался
    ('AAA@pytest.com', 'test1234', 'AAA', 201),  # зарегистрировался
    ('pytest2@pytest.com', 'test', 'pytest2', 400),  # пароль меньше 8 символов
    ('abcdefgh', 'test1234', 'pytest3', 422)  # неверный  формат почты
])
async def test_register_user(email, password, username, status_code, ac: AsyncClient):
    """Проверяет регистрацию пользователей."""
    response = await ac.post('/v1/auth/register', json={
        'email': email,
        'password': password,
        'username': username
    })

    assert response.status_code == status_code


@pytest.mark.parametrize('username, password, status_code', [
    ('test@test.com', 'test', 204),  # был создан моками, не зависит от теста регистрации
    ('AAA@pytest.com', 'test1234', 204),  # успешный вход, зависит от теста выше; создан для удобства
    ('AAA', 'test1234', 400),  # username, вместо пароля
    ('pytest@notfound.com', 'pytest', 400), # пытается зайти без регистрации
])
async def test_login_user(username, password, status_code, ac: AsyncClient):
    response = await ac.post(
        '/v1/auth/jwt/login',
        data={
            'username': username,
            'password': password
        }
    )

    assert response.status_code == status_code

# # $argon2id$v=19$m=65536,t=3,p=4$som++HPyzGirFpXKj299fg$LEA48cEK6QBVQtgNn/BF3l0THcdQexsH0PA+Uslc+H0    hash testuser
