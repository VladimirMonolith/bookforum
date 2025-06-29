import pytest

from app.reviews.dao import ReviewDAO


@pytest.mark.parametrize('text, user_id, book_id, update_text', [
    ('Лучшее, что читал', 2, 1, {'text': 'Лучшее, что читал!!!'}),
])
async def test_review_crud(text, user_id, book_id, update_text):
    """Проверяет crud-операции отзыва."""
    # Добавление отзыва
    new_review = await ReviewDAO.add_review_object(
        text=text,
        user_id=user_id,
        book_id=book_id
    )
    assert new_review['user_id'] == user_id
    assert new_review['book_id'] == book_id

    # Проверка добавления отзыва
    new_review = await ReviewDAO.get_object(id=new_review['id'])
    assert new_review is not None

    # Проверка обновления отзыва
    updated_review = await ReviewDAO.update_object(
       update_data=update_text,
       id=new_review['id']
    )
    assert updated_review.text == update_text['text']

    # Проверка удаления отзыва
    await ReviewDAO.delete_object(id=new_review['id'])
    deleted_review = await ReviewDAO.get_object(id=new_review['id'])
    assert deleted_review is None
