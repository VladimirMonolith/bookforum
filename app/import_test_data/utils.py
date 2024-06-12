from datetime import datetime
from typing import Iterable

from app.books.dao import BookDAO
from app.genres.dao import GenreDAO
from app.logger import logger
from app.reviews.dao import ReviewDAO
from app.users.dao import UserDAO

TABLE_MODEL_MAP = {
    'books': BookDAO,
    'genres': GenreDAO,
    'reviews': ReviewDAO,
    'users': UserDAO
}


def convert_csv_to_postgres_format(csv_iterable: Iterable):
    """Конвертирует csv в формат PosgreSQL."""
    try:
        data = []
        for row in csv_iterable:
            for key, value in row.items():
                if value.isdigit():
                    row[key] = int(value)
                elif 'registrated' in key:
                    row[key] = datetime.strptime(value, '%Y-%m-%d')
            data.append(row)
        return data
    except Exception as error:
        logger.error(f'An error has occurred: {error}', exc_info=True)
        return None
