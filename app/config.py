from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
# from dotenv import dotenv_values


class Settings(BaseSettings):
    """Класс для работы с переменными окружения."""

    MODE: Literal['DEV', 'TEST', 'PROD', 'INFO', 'DEBUG']
    LOG_LEVEL: str

    POSTGRES_DB_NAME: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    TEST_POSTGRES_DB_NAME: str
    TEST_POSTGRES_HOST: str
    TEST_POSTGRES_PORT: int
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str

    SECRET_KEY: str
    ALGORITHM: str

    REDIS_HOST: str
    REDIS_PORT: str

    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str

    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_HOST: str
    SMTP_PORT: int

    SECRET: str
    PASSWORD: str

    # SENTRY: str

    @property
    def DATABASE_URL(self):
        return (f'postgresql+asyncpg://{self.POSTGRES_USER}:'
                f'{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:'
                f'{self.POSTGRES_PORT}/{self.POSTGRES_DB_NAME}')

    @property
    def TEST_DATABASE_URL(self):
        return (f'postgresql+asyncpg://{self.TEST_POSTGRES_USER}:'
                f'{self.TEST_POSTGRES_PASSWORD}@{self.TEST_POSTGRES_HOST}:'
                f'{self.TEST_POSTGRES_PORT}/{self.TEST_POSTGRES_DB_NAME}')

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

# Было добавлено, потому что брались некорректные переменные окружения
# env_vars = dotenv_values('.env')
# settings = Settings(**env_vars)


settings = Settings()
