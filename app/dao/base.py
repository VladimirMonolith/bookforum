from typing import Type

from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.database import Base, async_session
from app.logger import logger


class BaseDAO:
    """Класс для работы с объектами БД."""

    model: Type[Base]

    @classmethod
    async def get_all_objects(cls, **kwargs):
        """Возвращает все объекты модели."""
        try:
            async with async_session() as session:
                query = (select(cls.model.__table__.columns)
                         .filter_by(**kwargs)
                         .order_by(cls.model.id))
                result = await session.execute(query)
                return result.mappings().all()
        except (SQLAlchemyError, Exception) as error:
            if isinstance(error, SQLAlchemyError):
                message = 'Database Exception'
            elif isinstance(error, Exception):
                message = 'Unknown Exception'
            message += ': Не удается получить данные.'

            logger.error(
                message,
                extra={'table': cls.model.__tablename__},
                exc_info=True
            )
            return None

    @classmethod
    async def get_object(cls, **kwargs):
        """Возвращает объект модели."""
        try:
            async with async_session() as session:
                query = select(cls.model.__table__.columns).filter_by(**kwargs)
                result = await session.execute(query)
                return result.mappings().one_or_none()
        except (SQLAlchemyError, Exception) as error:
            if isinstance(error, SQLAlchemyError):
                message = 'Database Exception'
            elif isinstance(error, Exception):
                message = 'Unknown Exception'
            message += ': Не удается получить данные.'

            logger.error(
                message,
                extra={'table': cls.model.__tablename__},
                exc_info=True
            )
            return None

    @classmethod
    async def add_objects(cls, *data):
        """Добавляет объекты в БД."""
        try:
            query = insert(cls.model).values(*data).returning(cls.model.id)
            async with async_session() as session:
                result = await session.execute(query)
                await session.commit()
                return result.mappings().first()
        except (SQLAlchemyError, Exception) as error:
            if isinstance(error, SQLAlchemyError):
                message = 'Database Exception'
            elif isinstance(error, Exception):
                message = 'Unknown Exception'
            message += ': Не удается добавить данные.'

            logger.error(
                message,
                extra={'table': cls.model.__tablename__},
                exc_info=True
            )
            return None

    @classmethod
    async def add_object(cls, **kwargs):
        """Добавляет объект в БД."""
        try:
            async with async_session() as session:
                query = insert(cls.model).values(**kwargs)
                await session.execute(query)
                await session.commit()
                return 'Данные успешно добавлены.'
        except (SQLAlchemyError, Exception) as error:
            if isinstance(error, SQLAlchemyError):
                message = 'Database Exception'
            elif isinstance(error, Exception):
                message = 'Unknown Exception'
            message += ': Не удается добавить данные.'

            logger.error(
                message,
                extra={'table': cls.model.__tablename__},
                exc_info=True
            )
            return None

    @classmethod
    async def update_object(cls, update_data, **kwargs):
        """Позволяет обновлять данные объекта."""
        try:
            async with async_session() as session:
                query = select(cls.model).filter_by(**kwargs)
                result = await session.execute(query)
                result = result.scalar_one_or_none()

                # Поддержка Pydantic-схем
                if hasattr(update_data, 'dict'):
                    new_data = update_data.model_dump(exclude_unset=True)
                # Поддержка обычных словарей
                elif isinstance(update_data, dict):
                    new_data = update_data

                for key, value in new_data.items():
                    setattr(result, key, value)
                session.add(result)
                await session.commit()
                await session.refresh(result)
                return result
        except (SQLAlchemyError, Exception) as error:
            if isinstance(error, SQLAlchemyError):
                message = 'Database Exception'
            elif isinstance(error, Exception):
                message = 'Unknown Exception'
            message += ': Не удается обновить данные.'

            logger.error(
                message,
                extra={'Database table': cls.model.__tablename__},
                exc_info=True
            )
            return None

    @classmethod
    async def delete_object(cls, **kwargs):
        """Удаляет объект из БД."""
        try:
            async with async_session() as session:
                query = select(cls.model).filter_by(**kwargs)
                result = await session.execute(query)
                result = result.scalar()
                await session.delete(result)
                await session.commit()
                return 'Удаление успешно завершено.'
        except (SQLAlchemyError, Exception) as error:
            if isinstance(error, SQLAlchemyError):
                message = 'Database Exception'
            elif isinstance(error, Exception):
                message = 'Unknown Exception'
            message += ': Не удается удалить данные.'

            logger.error(
                message,
                extra={'table': cls.model.__tablename__},
                exc_info=True
            )
            return None
