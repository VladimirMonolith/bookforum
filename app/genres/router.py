from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from fastapi_versioning import version

from app.exceptions import (
    DatabaseErrorException,
    NotFoundException,
    ObjectAlreadyExistsException
)
from app.users.manager import current_superuser
from app.users.models import User

from .dao import GenreDAO
from .schemas import GenreCreate, GenreRead, GenreUpdate

router = APIRouter(
    prefix='/genres',
    tags=['genres']
)


@router.post('')
@version(1)
async def create_genre(
    data: GenreCreate, user: User = Depends(current_superuser)
):
    """Позволяет добавить новый жанр."""
    genre_exists = await GenreDAO.get_object(name=data.name)

    if genre_exists:
        raise ObjectAlreadyExistsException
    new_genre = await GenreDAO.add_object(**data.model_dump())

    if not new_genre:
        raise DatabaseErrorException(
            detail='Не удалось добавить запись в базу данных.'
        )
    return new_genre


@router.get('', response_model=List[GenreRead])
@version(1)
@cache(expire=60)
async def get_all_genres():
    """Возвращает все жанры."""
    genres = await GenreDAO.get_all_objects()

    if not genres:
        raise NotFoundException
    return genres


@router.get('/{genre_id}', response_model=GenreRead)
@version(1)
async def get_genre(genre_id: int):
    """Возвращает конкретный жанр."""
    genre = await GenreDAO.get_object(id=genre_id)

    if not genre:
        raise NotFoundException
    return genre


@router.patch('/{genre_id}', response_model=GenreRead)
@version(1)
async def update_genre(
    genre_id: int,
    update_data: GenreUpdate,
    user: User = Depends(current_superuser)
):
    """Позволяет обновить название жанра."""
    genre = await GenreDAO.update_object(
        update_data=update_data, id=genre_id
    )

    if not genre:
        raise DatabaseErrorException(detail='Не удалось обновить данные.')
    return genre


@router.delete('/{genre_id}')
@version(1)
async def delete_genre(
    genre_id: int,
    user: User = Depends(current_superuser)
):
    """Позволяет удалить жанр."""
    result = await GenreDAO.delete_object(id=genre_id)

    if not result:
        raise DatabaseErrorException(
            detail='Не удалось удалить запись из базы данных.'
        )
    return result
