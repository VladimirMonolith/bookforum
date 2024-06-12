import smtplib

from pydantic import EmailStr

from app.config import settings
from app.tasks.celery_config import celery
from app.tasks.email_templates import create_review_confirmation_template


@celery.task(name='review_confirmation_email')
def send_review_confirmation_email(
    review: dict,
    username: str,
    email_to: EmailStr,
    book_title: str
):
    """Отправляет email с подтверждением бронирования."""
    email_to_user = settings.SMTP_USER
    email_content = create_review_confirmation_template(
        review=review, username=username,
        email_to=email_to_user, book_title=book_title
    )
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(email_content)
