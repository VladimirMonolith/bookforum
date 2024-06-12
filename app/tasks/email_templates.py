from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def create_review_confirmation_template(
    review: dict,
    username: str,
    email_to: EmailStr,
    book_title: str
):
    """Формирует email об оставленном отзыве."""
    email = EmailMessage()

    email['Subject'] = 'Информация об оставленном отзыве.'
    email['From'] = settings.SMTP_USER
    email['To'] = email_to

    email.set_content(
        f"""
        <h1>Информирование об оставленном отзыве.</h1>
        Здравствуйте, {username}!
        Вы оставили отзыв на нашем сайте на книгу - {book_title}.
        Благодарим за доверие и надеемся на дальнейшее сотрудничество.
        """,
        subtype='html'
    )
    return email

# {review['book'].name}
