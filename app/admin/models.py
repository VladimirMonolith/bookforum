from sqladmin import ModelView

from app.books.models import Book
from app.genres.models import Genre
from app.reviews.models import Review
from app.users.models import User


class UserAdmin(ModelView, model=User):
    """Класс для отображения пользователей в админке."""

    column_list = [c.name for c in User.__table__.c]
    column_details_exclude_list = [User.hashed_password]
    column_list += [User.reviews]
    can_delete = True
    name = 'Пользователь'
    name_plural = 'Пользователи'
    icon = 'fa-solid fa-user'


class BookAdmin(ModelView, model=Book):
    """Класс для отображения категорий в админке."""

    column_list = [c.name for c in Book.__table__.c]
    column_list += [Book.genres, Book.reviews]
    name = 'Книга'
    name_plural = 'Книги'
    icon = 'fa-solid fa-book'


class GenreAdmin(ModelView, model=Genre):
    """Класс для отображения жанров в админке."""

    column_list = [c.name for c in Genre.__table__.c]
    column_list += [Genre.books]
    name = 'Жанр'
    name_plural = 'Жанры'
    icon = 'fa-solid fa-icons'


class ReviewAdmin(ModelView, model=Review):
    """Класс для отображения отзывов в админке."""

    column_list = [
        c.name if c.name != 'text' else c.name[:25] for c in Review.__table__.c
    ]
    column_list += [Review.author, Review.book]
    name = 'Отзыв'
    name_plural = 'Отзывы'
    icon = 'fa-solid fa-pen'
