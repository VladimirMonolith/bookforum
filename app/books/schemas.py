from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.genres.schemas import GenreRead
from app.reviews.schemas import ReviewRead


class BookRead(BaseModel):
    """Модель отображения книги."""

    id: int
    title: str
    authors: str
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class BookReadDetail(BaseModel):
    """Модель отображения подробных данных о книге."""

    id: int
    title: str
    authors: str
    description: Optional[str]
    genres: List[GenreRead]
    reviews: List[ReviewRead]

    model_config = ConfigDict(from_attributes=True)


class BookCreate(BaseModel):
    """Модель для добавления книги."""

    title: str
    authors: str
    description: Optional[str] = None


class BookUpdate(BaseModel):
    """Модель для обновления книги."""

    title: Optional[str] = None
    authors: Optional[str] = None
    description: Optional[str] = None
