import json

import aio_pika

from app.config import settings


async def send_review_task_to_queue(payload: dict):
    connection = await aio_pika.connect_robust(
        f'amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}/'
    )
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(payload).encode(),
                content_type='application/json'
            ),
            routing_key='review_email'
        )
