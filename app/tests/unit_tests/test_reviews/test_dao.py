import pytest

from app.reviews.dao import ReviewDAO


@pytest.mark.parametrize('id, is_exist', [
    (1, True),
    (2, True),
    (55, False)
])
async def test_find_review_by_id(id, is_exist):
    """Проверяет существование отзыва."""
    review = await ReviewDAO.get_object(id=id)

    if is_exist:
        assert review
        assert review['id'] == id
    else:
        assert not review
