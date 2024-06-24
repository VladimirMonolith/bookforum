import time
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.models import BookAdmin, GenreAdmin, ReviewAdmin, UserAdmin
from app.books.router import router as books_router
from app.config import settings
from app.database import engine
from app.genres.router import router as genres_router
from app.import_test_data.router import router as test_data_router
from app.logger import logger
from app.prometheus.router import router as prometheus_router
from app.reviews.router import router as reviews_router
from app.users.config import auth_backend
from app.users.manager import fastapi_users
from app.users.schemas import UserCreate, UserRead, UserUpdate

sentry_sdk.init(
    dsn=f'{settings.SENTRY}',
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0
)

app = FastAPI(title='bookforum')


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix='/auth',
    tags=['auth'],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix='/auth',
    tags=['auth'],
)

app.include_router(
    fastapi_users.get_users_router(
        UserRead, UserUpdate, requires_verification=True
    ),
    prefix='/users',
    tags=['users'],
)

app.include_router(test_data_router)
app.include_router(books_router)
app.include_router(genres_router)
app.include_router(reviews_router)
app.include_router(prometheus_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f'Service {app.title} started.')
    redis = aioredis.from_url(
        f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}',
        encoding='utf8',
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
    yield

app = VersionedFastAPI(
    app,
    version_format='{major}',
    prefix_format='/v{major}',
    lifespan=lifespan
)

admin = Admin(
    app=app, engine=engine, authentication_backend=authentication_backend
)

admin.add_view(UserAdmin)
admin.add_view(BookAdmin)
admin.add_view(GenreAdmin)
admin.add_view(ReviewAdmin)


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    """Добавляет заголовок со временем выполнения запроса."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(
        'Request handlinf time',
        extra={'process_time': round(process_time, 4)}
    )
    return response

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=['.*admin.*', '/metrics'],
)
instrumentator.instrument(app).expose(app)


