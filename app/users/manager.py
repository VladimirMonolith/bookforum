from typing import Any, Dict, Optional, Union

from fastapi import Depends, Request, Response
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    InvalidPasswordException
)

from app.config import settings

from .config import auth_backend
from .models import User
from .schemas import UserCreate
from .utils import get_user_db


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.PASSWORD
    verification_token_secret = settings.PASSWORD

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ):
        if len(password) < 8:
            raise InvalidPasswordException(
                reason='Длина пароля должна быть не менее 8 символов.'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Пароль не должен содержать email.'
            )

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ):
        print(f'Пользователь c id {user.id} был зарегистрирован.')

    async def on_after_update(
        self,
        user: User,
        update_dict: Dict[str, Any],
        request: Optional[Request] = None,
    ):
        print(f'Пользователь c id {user.id} был обновлен '
              f'следующими данными: {update_dict}.')

    async def on_after_login(
        self,
        user: User,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ):
        print(f'Пользователь c id {user.id} вошёл в систему.')

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f'Запрошена верификация для пользователя с id {user.id}.'
              f'Токен верификации: {token}')

    async def on_after_verify(
        self, user: User, request: Optional[Request] = None
    ):
        print(f'Пользователь c id {user.id} был верифицирован.')

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f'Пользователь с id {user.id} забыл свой пароль. '
              f'Токен сброса пароля: {token}')

    async def on_after_reset_password(
            self, user: User,
            request: Optional[Request] = None
            ):
        print(f'Пользователь c id {user.id} сбросил пароль.')

    async def on_before_delete(
            self, user: User,
            request: Optional[Request] = None
            ):
        print(f'Пользователь c id {user.id} собирается удалить профиль.')

    async def on_after_delete(
            self, user: User,
            request: Optional[Request] = None
            ):
        print(f'Пользователь c id {user.id} был успешно удалён.')


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
