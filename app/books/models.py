from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.genres.models import Genre
    from app.reviews.models import Review


class BooksGenres(Base):
    __tablename__ = 'books_genres'

    book_id: Mapped[int] = mapped_column(
        ForeignKey('books.id'),
        primary_key=True
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey('genres.id'),
        primary_key=True
    )


class Book(Base):
    """Модель книги."""

    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(length=150))
    authors: Mapped[str]
    description: Mapped[Optional[str]]
    genres: Mapped[List['Genre']] = relationship(
        back_populates='books', secondary=BooksGenres.__table__
    )
    reviews: Mapped[List['Review']] = relationship(
        back_populates='book'
    )

    def __str__(self):
        return f'Книга:id - {self.id}, название - {self.title}'
