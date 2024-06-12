from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from fastapi_versioning import version
from pydantic import TypeAdapter

from app.books.dao import BookDAO
from app.exceptions import (
    DatabaseErrorException,
    NotFoundException,
    ObjectAlreadyExistsException
)
from app.tasks.tasks import send_review_confirmation_email
from app.users.manager import current_active_user
from app.users.models import User

from .dao import ReviewDAO
from .schemas import ReviewCreate, ReviewRead, ReviewUpdate

router = APIRouter(
    prefix='/reviews',
    tags=['reviews']
)


@router.post('')
@version(1)
async def create_review(
    data: ReviewCreate, user: User = Depends(current_active_user)
):
    """Позволяет добавить новый отзыв текущего пользователя."""
    review_exists = await ReviewDAO.get_object(
        user_id=user.id, book_id=data.book_id
    )

    if review_exists:
        raise ObjectAlreadyExistsException

    review = await ReviewDAO.add_review_object(
        text=data.text,
        book_id=data.book_id,
        user_id=user.id
    )

    if not review:
        raise DatabaseErrorException(
            detail='Не удалось добавить запись в базу данных.'
        )

    book = await BookDAO.get_object(id=data.book_id)

    if not book:
        raise NotFoundException

    review_dict = (
        TypeAdapter(ReviewRead).validate_python(review).model_dump()
    )

    send_review_confirmation_email.delay(
        review=review_dict,
        username=user.username,
        email_to=user.email,
        book_title=book.title
    )
    return review


@router.get('', response_model=List[ReviewRead])
@version(1)
@cache(expire=60)
async def get_all_reviews(user: User = Depends(current_active_user)):
    """Возвращает все отзывы текущего пользователя."""
    reviews = await ReviewDAO.get_all_objects(user_id=user.id)

    if not reviews:
        raise NotFoundException
    return reviews


@router.get('/{review_id}', response_model=ReviewRead)
@version(1)
async def get_review(
    review_id: int,
    user: User = Depends(current_active_user)
):
    """Возвращает конкретный отзыв текущего пользователя."""
    review = await ReviewDAO.get_object(id=review_id, user_id=user.id)

    if not review:
        raise NotFoundException
    return review


@router.patch('/{review_id}', response_model=ReviewRead)
@version(1)
async def update_review(
    review_id: int,
    update_data: ReviewUpdate,
    user: User = Depends(current_active_user)
):
    """Позволяет обновить содержание конкретного отзыва текущего пользователя."""
    review = await ReviewDAO.update_object(
        update_data=update_data, id=review_id, user_id=user.id
    )

    if not review:
        raise DatabaseErrorException(detail='Не удалось обновить данные.')
    return review


@router.delete('/{review_id}')
@version(1)
async def delete_review(
    review_id: int,
    user: User = Depends(current_active_user)
):
    """Позволяет удалить конкретный отзыв текущего пользователя."""
    result = await ReviewDAO.delete_object(id=review_id, user_id=user.id)

    if not result:
        raise DatabaseErrorException(
            detail='Не удалось удалить запись из базы данных.'
        )
    return result
