import asyncio
import json
import smtplib

import aio_pika

from app.config import settings
from app.tasks.email_templates import create_review_confirmation_template

# Запускается отдельно - python app/tasks/consumer.py


async def main():
    connection = await aio_pika.connect_robust(
        f'amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}/'
    )
    channel = await connection.channel()
    queue = await channel.declare_queue('review_email', durable=True)

    async with queue.iterator() as queue_iterator:
        async for message in queue_iterator:
            async with message.process():
                payload = json.loads(message.body)
                email = create_review_confirmation_template(
                    review=payload['review'],
                    username=payload['username'],
                    email_to=payload['email_to'],
                    book_title=payload['book_title']
                )
                with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                    server.send_message(email)

if __name__ == '__main__':
    asyncio.run(main())
