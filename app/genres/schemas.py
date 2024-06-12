from typing import Optional

from pydantic import BaseModel, ConfigDict


class GenreRead(BaseModel):
    """Модель отображения жанра."""

    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class GenreCreate(BaseModel):
    """Модель для добавления жанра."""

    name: str


class GenreUpdate(BaseModel):
    """Модель для обновления жанра."""

    name: Optional[str] = None
