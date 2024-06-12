from app.dao.base import BaseDAO

from .models import Genre


class GenreDAO(BaseDAO):
    model = Genre
