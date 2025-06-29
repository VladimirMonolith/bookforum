import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('text, book_id, status_code', [
    ('Amazing!', 2, 200),
    ('Else one', 2, 409)
])
async def test_add_and_get_review(
    text, book_id, status_code, authenticated_ac: AsyncClient
):
    """Проверяет добавление отзыва, вариант 1."""
    # Получаем отзывы до добавления нового
    response = await authenticated_ac.get('/v1/reviews')
    assert response.status_code == 200
    initial_reviews = len(response.json())

    # Добавляем новый отзыв
    response = await authenticated_ac.post('/v1/reviews', json={
        'text': text,
        'book_id': book_id
    })

    assert response.status_code == status_code

    # Получаем отзывы после добавления
    response = await authenticated_ac.get('/v1/reviews')
    assert response.status_code == 200
    new_reviews = response.json()

    # Если статус успешный, проверяем, что отзыв добавился
    if status_code == 200:
        assert len(new_reviews) == initial_reviews + 1
        assert any(
            review['text'] == text and review['book_id'] == book_id
            for review in new_reviews
        )
    else:
        # Если неуспешный, то количество отзывов не изменилось
        assert len(new_reviews) == initial_reviews


@pytest.mark.parametrize('text, book_id, status_code', [
    ('Amazing!', 2, 200),
    ('Else one', 2, 409)
])
async def test_add_and_get_review_2(
    text, book_id, status_code, authenticated_ac: AsyncClient
):
    """Проверяет добавление отзыва, вариант 2."""
    # Добавляем отзыв
    response = await authenticated_ac.post('/v1/reviews', json={
        'text': text,
        'book_id': book_id
    })
    assert response.status_code == status_code

    # Если статус успешный, проверяем, что отзыв добавился
    if status_code == 200:
        created_review_id = response.json()['id']
        # Получаем по id
        response = await authenticated_ac.get(f'/v1/reviews/{created_review_id}')
        assert response.status_code == 200
        review = response.json()
        assert review['id'] == created_review_id
        assert review['text'] == 'Amazing!'
    else:
        # Если неуспешный, то количество отзывов не изменилось
        assert 'id' not in response.json()


async def test_get_and_delete_review(authenticated_ac: AsyncClient):
    """Проверяет удаление отзывов, вариант 1."""
    # Получаем отзывы
    response = await authenticated_ac.get('/v1/reviews')
    assert response.status_code == 200
    existing_reviews = [review['id'] for review in response.json()]

    # Удаляем все
    for review_id in existing_reviews:
        response = await authenticated_ac.delete(
            f'/v1/reviews/{review_id}',
        )

    response = await authenticated_ac.get('/v1/reviews')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Данные не найдены.'

    # Более правильно проверять
    # assert len(response.json()) == 0
    # для этого нужно убрать проверки
    # if not <>:
    #     raise NotFoundException
    # из всех эндпойнтов


async def test_get_and_delete_review_2(authenticated_ac: AsyncClient):
    """Проверяет удаление отзыва, вариант 2."""
    # Добавляем отзыв
    response = await authenticated_ac.post('/v1/reviews', json={
        'text': 'For delete!',
        'book_id': 2
    })
    assert response.status_code == 200
    review_id = response.json()['id']

    # Удаляем отзыв
    response = await authenticated_ac.delete(f'/v1/reviews/{review_id}')
    assert response.status_code == 200

    # Проверяем, что отзыв удален
    response = await authenticated_ac.get(f'/v1/reviews/{review_id}')
    assert response.status_code == 404


@pytest.mark.parametrize('text, book_id, new_text, status_code', [
    ('Старый отзыв!', 2, 'Обновленный отзыв!', 200),
])
async def test_patch_review(
    text, book_id, new_text, status_code, authenticated_ac: AsyncClient
):
    """Проверяет обновление отзыва."""
    # Добавляем отзыв
    response = await authenticated_ac.post('/v1/reviews', json={
        'text': text,
        'book_id': book_id
    })
    assert response.status_code == 200
    review_id = response.json()['id']

    # Обновляем текст
    response = await authenticated_ac.patch(f'/v1/reviews/{review_id}', json={
        'text': new_text
    })
    assert response.status_code == status_code
    assert response.json()['text'] == new_text
