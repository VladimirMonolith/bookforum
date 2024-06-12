from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from app.dao.base import BaseDAO
from app.database import async_session
from app.logger import logger

from .models import Book


class BookDAO(BaseDAO):
    model = Book

    @classmethod
    async def get_book_with_details(
        cls,
        book_id: int
    ):
        """Возвращает информацию о книге с её жанрами и отзывами."""
        try:
            async with async_session() as session:
                book = (select(Book)
                        .options(joinedload(Book.reviews), joinedload(Book.genres))
                        .filter(Book.id == book_id))
                book = await session.execute(book)
                return book.unique().scalar_one_or_none()
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            logger.error(
                message,
                extra={'Database table': cls.model.__tablename__},
                exc_info=True
            )
            return None
