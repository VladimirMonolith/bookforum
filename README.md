# Cервис Bookforum

![Python](https://img.shields.io/badge/Python-464646?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-464646?style=flat-square&logo=fastapi)
![Асинхронность](https://img.shields.io/badge/Асинхронность-464646?style=flat-square)
![Cookies](https://img.shields.io/badge/Cookies-464646?style=flat-square)
![JWT](https://img.shields.io/badge/JWT-464646?style=flat-square&logo=JSON%20web%20tokens)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-464646?style=flat-square&logo=postgreSQL)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-464646?style=flat-square&logo=sqlalchemy)
![Alembic](https://img.shields.io/badge/Alembic-464646?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-464646?style=flat-square&logo=docker)
![Redis](https://img.shields.io/badge/Redis-464646?style=flat-square&logo=redis)
![Celery](https://img.shields.io/badge/Celery-464646?style=flat-square&logo=celery)
![Sentry](https://img.shields.io/badge/-Sentry-464646?style=flat-square&logo=sentry)
![Prometheus](https://img.shields.io/badge/-Prometheus-464646?style=flat-square&logo=prometheus)
![Grafana](https://img.shields.io/badge/-Grafana-464646?style=flat-square&logo=grafana)
![NGINX](https://img.shields.io/badge/NGINX-464646?style=flat-square&logo=nginx)
![Uvicorn](https://img.shields.io/badge/Uvicorn-464646?style=flat-square)
![Gunicorn](https://img.shields.io/badge/Gunicorn-464646?style=flat-square&logo=gunicorn)

## Описание

API книжного форума.

### Доступный функционал

- Регистрация пользователей с помощью библиотеки fastapi-users.
- Аутентификация реализована с помощью куков и JWT-токена.
- У неаутентифицированных пользователей доступ к API только на уровне чтения.
- Создание объектов разрешено только аутентифицированным пользователям.
- Возможность получения подробной информации о себе.
- Загрузка тестовых данных в БД.
- Возможность получить подробную информацию о конкретной книге и выполнить операции CRUD.
- Возможность осуществить операции CRUD для жанров.
- Возможность осуществить операции CRUD для отзывов конкретного пользователя.
- Управление пользователями с помощью функционала библиотеки fastapi-users.
- Отправка email с подтверждением отзыва пользователя посредством Celery.
- Возможность администрирования сервиса.
- Версионирование API.
- Кеширование/брокер задач с помощью Redis.
- Для защиты от DDoS-атак используется библиотека slowapi
- Логирование посредством кастомного логгера.
- Мониторинг ошибок с помощью Sentry.
- Сбор метрик с помощью Prometheus.
- Визуализация метрик посредством Grafana.
- Возможность развернуть проект в Docker-контейнерах.
- Возможность использовать NGINX при развертывании проекта в Docker-контейнерах, на VPS или выделенном сервере.

#### Технологии

- Python 3.9
- FastAPI
- fastapi-cache2
- Асинхронность
- Cookies
- JWT
- Alembic
- SQLAlchemy
- Docker
- PostgreSQL
- Asyncpg
- CORS
- Redis
- Celery
- Flower
- Sentry
- Prometheus
- Grafana
- NGINX
- Uvicorn
- Gunicorn

#### Локальный запуск проекта

- Предварительно необходимо установить Docker и Redis для вашей системы.

- Склонировать репозиторий:

```bash
git clone <название репозитория>
```

Cоздать и активировать виртуальное окружение:

Команды для установки виртуального окружения на Mac или Linux:

```bash
python3 -m venv env
source env/bin/activate
```

Команды для Windows:

```bash
python -m venv venv
source venv/Scripts/activate
```

- Создать файл .env по образцу:

```bash
cp .env_local_example .env
```

- Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

- Для создания миграций выполнить команду:

```bash
alembic init migrations
```

- В папку migrations в env файл вставьте следующий код:

```bash
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.books.models import Book
from app.config import settings
from app.database import Base
from app.genres.models import Genre
from app.reviews.models import Review
from app.users.models import User

config = context.config

config.set_main_option('sqlalchemy.url', f'{settings.DATABASE_URL}?async_fallback=True')

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
```

- Инициализировать БД:

``` bash
alembic revision --autogenerate -m "comment"   
```

- Применить миграцию:

``` bash
alembic upgrade head 
```

- Запустить проект:

``` bash
uvicorn app.main:app --reload    
```

- Запустить Redis:

``` bash
redis-server.exe 
redis-cli.exe  
```

- Запустить Celery:

``` bash
celery -A app.tasks.celery_config:celery worker --loglevel=INFO --pool=solo
```

- Запустить Flower:

``` bash
celery -A app.tasks.tasks:celery flower
```

##### Локально документация доступна по адресу: <http://localhost:8000/v1/docs/>

#### Запуск в контейнерах Docker

- Находясь в главной директории проекта:

- Создать файл .env_docker по образцу:

```bash
cp .env_docker_example .env_docker 
```

- **Если планируете задействовать NGINX:**

```
Согласно примечаниям в файле docker-compose.yml закомментируйте код внутри него
```

- Запустить проект:

``` bash
docker-compose up -d --build  
```

##### В контейнерах Docker документация доступна по адресу: <http://localhost:7777/v1/docs/>

##### Полный список запросов API находится в документации

##### Автор

Гут Владимир - [https://github.com/VladimirMonolith](http://github.com/VladimirMonolith)