from typing import Optional

from fastapi_users import schemas
from pydantic import ConfigDict, EmailStr


class UserRead(schemas.BaseUser[int]):
    """Модель отображения пользователя."""

    id: int
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserCreate(schemas.BaseUserCreate):
    """Модель создания пользователя."""

    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    password: str


class UserUpdate(schemas.BaseUserUpdate):
    """Модель, позволяющая пользователю обновлять свои данные."""

    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
