from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy
)

from app.config import settings

cookie_transport = CookieTransport(
    cookie_name='bookforum',
    cookie_max_age=3600,
    # В тестах без HTTPS кука должна быть не secure
    # httpx + fastapi-users эта настройка обязательна для pytest
    cookie_secure=False
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
