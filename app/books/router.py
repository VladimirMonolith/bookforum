from typing import List

from fastapi import APIRouter, Depends, Request
from fastapi_cache.decorator import cache
from fastapi_versioning import version

from app.exceptions import (
    DatabaseErrorException,
    NotFoundException,
    ObjectAlreadyExistsException
)
from app.rate_limiting import limiter
from app.users.manager import current_superuser
from app.users.models import User

from .dao import BookDAO
from .schemas import BookCreate, BookRead, BookReadDetail, BookUpdate

router = APIRouter(
    prefix='/books',
    tags=['books']
)


@router.post('')
@version(1)
async def create_book(
    data: BookCreate, user: User = Depends(current_superuser)
):
    """Позволяет добавить новую книгу."""
    book_exists = await BookDAO.get_object(title=data.title)

    if book_exists:
        raise ObjectAlreadyExistsException
    new_book = await BookDAO.add_object(**data.model_dump())

    if not new_book:
        raise DatabaseErrorException(
            detail='Не удалось добавить запись в базу данных.'
        )
    return new_book


@router.get('', response_model=List[BookRead])
@version(1)
@cache(expire=60)
async def get_all_books():
    """Возвращает все книги."""
    books = await BookDAO.get_all_objects()

    if not books:
        raise NotFoundException
    return books


@router.get('/{book_id}', response_model=BookReadDetail)
@version(1)
@limiter.limit('1/minute')
async def get_book(book_id: int, request: Request):
    """Возвращает подробную информацию о конкретной книге."""
    book = await BookDAO.get_book_with_details(book_id=book_id)

    if not book:
        raise NotFoundException
    return book


@router.patch('/{book_id}', response_model=BookRead)
@version(1)
async def update_book(
    book_id: int,
    update_data: BookUpdate,
    user: User = Depends(current_superuser)
):
    """Позволяет обновить название книги."""
    book = await BookDAO.update_object(
        update_data=update_data, id=book_id
    )

    if not book:
        raise DatabaseErrorException(detail='Не удалось обновить данные.')
    return book


@router.delete('/{book_id}')
@version(1)
async def delete_book(
    book_id: int,
    user: User = Depends(current_superuser)
):
    """Позволяет удалить книгу."""
    result = await BookDAO.delete_object(id=book_id)

    if not result:
        raise DatabaseErrorException(
            detail='Не удалось удалить запись из базы данных.'
        )
    return result
