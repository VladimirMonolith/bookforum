from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from app.dao.base import BaseDAO
from app.database import async_session
from app.logger import logger

from .models import Review


class ReviewDAO(BaseDAO):
    model = Review

    @classmethod
    async def add_review_object(
        cls,
        text: str,
        user_id: int,
        book_id: int
    ):
        """Добавляет объект отзыва в БД."""
        try:
            async with async_session() as session:
                review = insert(Review).values(
                    text=text, book_id=book_id, user_id=user_id
                ).returning(
                    Review.id, Review.text,
                    Review.user_id, Review.book_id
                )
                review = await session.execute(review)
                await session.commit()
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            logger.error(
                message,
                extra={'Database table': cls.model.__tablename__},
                exc_info=True
            )
            return None
        return review.mappings().one()
