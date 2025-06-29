from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


if settings.MODE == 'TEST':
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {'poolclass': NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}

print(f'Используемая БД: {DATABASE_URL}')

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
engine_nullpool = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
async_session_nullpool = async_sessionmaker(
    bind=engine_nullpool, class_=AsyncSession, expire_on_commit=False
)

# engine = create_async_engine(settings.DATABASE_URL)
# async_session = async_sessionmaker(
#     bind=engine, class_=AsyncSession, expire_on_commit=False
# )


class Base(DeclarativeBase):
    """Базовый класс БД."""

    pass
