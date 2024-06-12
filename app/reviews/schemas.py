from typing import Optional

from pydantic import BaseModel, ConfigDict


class ReviewRead(BaseModel):
    """Модель отображения отзывов."""

    id: int
    text: str
    user_id: int
    book_id: int

    model_config = ConfigDict(from_attributes=True)


class ReviewCreate(BaseModel):
    """Модель для добавления отзывов."""

    text: str
    book_id: int


class ReviewUpdate(BaseModel):
    """Модель для обновления отзывов."""

    text: Optional[str] = None
