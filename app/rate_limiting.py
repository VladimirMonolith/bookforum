from slowapi import Limiter
from slowapi.util import get_remote_address
from app.config import settings


limiter = Limiter(
    key_func=get_remote_address,
    application_limits=['1000/day'],
    default_limits=['20/minute'],
    enabled=True
)

limiter = Limiter(
    key_func=get_remote_address,
    application_limits=['1000/day'],
    default_limits=['20/minute'],
    storage_uri=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}',
    enabled=True
)
