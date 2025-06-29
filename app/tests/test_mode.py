from app.config import settings
from app.database import DATABASE_PARAMS, DATABASE_URL


def test_mode_is_test():
    """Проверяет, что мы работаем с тестовой БД."""
    print(f'Текущий режим работы: {settings.MODE}, подключение к БД: {DATABASE_URL}')
    print(f'{DATABASE_PARAMS}')
    assert settings.MODE == 'TEST', f"Expected MODE='TEST', got '{settings.MODE}'"
