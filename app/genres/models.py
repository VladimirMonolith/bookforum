from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.books.models import BooksGenres
from app.database import Base

if TYPE_CHECKING:
    from app.books.models import Book


class Genre(Base):
    """Модель жанра."""

    __tablename__ = 'genres'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=20))
    books: Mapped[List['Book']] = relationship(
        back_populates='genres', secondary=BooksGenres.__table__
    )

    def __str__(self):
        return f'Жанр:id - {self.id}, название - {self.name}'
