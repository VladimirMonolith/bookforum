
import asyncio
import json
from datetime import datetime

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert

from app.books.models import Book
from app.config import settings
from app.database import Base, async_session, engine
from app.genres.models import Genre
from app.main import app
from app.reviews.models import Review
from app.users.models import User

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend


@pytest.fixture(scope='session', autouse=True)
async def setup_database():
    """Инициализирует тестовую БД."""
    assert settings.MODE == 'TEST'

    async with engine.begin() as conn:
        # Удаление всех заданных нами таблиц из БД
        await conn.run_sync(Base.metadata.drop_all)
        # yield (БД очистится после всех тестов)
        # Добавление всех заданных нами таблиц из БД
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f'app/tests/mock_{model}.json', encoding='utf-8') as file:
            return json.load(file)

    books = open_mock_json('books')
    genres = open_mock_json('genres')
    users = open_mock_json('users')
    reviews = open_mock_json('reviews')

    for user in users:
        # SQLAlchemy не принимает дату в текстовом формате,
        # поэтому форматируем к datetime
        user['registrated'] = datetime.strptime(user['registrated'], '%Y-%m-%d')

    async with async_session() as session:
        for Model, values in [
            (User, users),
            (Book, books),
            (Genre, genres),
            (Review, reviews),
        ]:
            query = insert(Model).values(values)
            await session.execute(query)

        await session.commit()


# Взято из документации к pytest-asyncio
# Создаем новый event loop для прогона тестов
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def ac():
    "Асинхронный клиент для тестирования эндпойнтов"
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='session')
async def authenticated_ac():
    """Асинхронный аутентифицированный клиент для тестирования эндпойнтов."""
    # Инициализируем кеш, Redis должен быть поднят
    FastAPICache.init(InMemoryBackend(), prefix='fastapi-cache')

    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.post(
            '/v1/auth/jwt/login',
            data={
                'username': 'test@test.com',
                'password': 'test'
            }
        )

        print('LOGIN STATUS:', response.status_code)
        print('SET-COOKIE HEADER:', response.headers.get('set-cookie'))
        print('COOKIES IN CLIENT:', ac.cookies)

        assert response.status_code == 204, response.text
        assert 'bookforum' in ac.cookies, 'Кука bookforum не установлена!'

        yield ac

# Фикстура оказалась бесполезной(фикстура сессии SQLAlchemy)
# @pytest.fixture(scope='function')
# async def session():
#     async with async_session() as session:
#         yield session
