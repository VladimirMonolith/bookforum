from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.books.models import Book
    from app.users.models import User


class Review(Base):
    """Модель отзыва."""

    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(length=300))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))
    author: Mapped['User'] = relationship(back_populates='reviews')
    book: Mapped['Book'] = relationship(back_populates='reviews')

    def __str__(self):
        return f'Отзыв:id - {self.id}, содержание - {self.text[:25]}'
