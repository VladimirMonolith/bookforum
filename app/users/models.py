from datetime import date
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base

if TYPE_CHECKING:
    from app.reviews.models import Review


class User(Base):
    """Модель пользователя."""

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(length=30), unique=True)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True
    )
    first_name: Mapped[Optional[str]] = mapped_column(String(length=50))
    last_name: Mapped[Optional[str]] = mapped_column(String(length=100))
    registrated: Mapped[date] = mapped_column(default=func.current_date())
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True, nullable=True)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=True)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=True)
    reviews: Mapped[List['Review']] = relationship(back_populates='author')

    def __str__(self):
        return f'Пользователь: username - {self.username}, email - {self.email}'
