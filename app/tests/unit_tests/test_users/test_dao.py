import pytest

from app.users.dao import UserDAO


@pytest.mark.parametrize('email, is_exist', [
    ("test@test.com", True),
    ("artem@example.com", True),
    ("someone@someone.com", False)
])
async def test_find_user_by_email(email, is_exist):
    """Проверяет существование пользователя."""
    user = await UserDAO.get_object(email=email)

    if is_exist:
        assert user
        assert user['email'] == email
    else:
        assert not user
