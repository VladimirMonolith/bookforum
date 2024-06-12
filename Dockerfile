FROM python:3.9    

RUN mkdir /bookforum     

WORKDIR /bookforum    

COPY requirements.txt . 

RUN pip install -r requirements.txt

COPY . .

# предоставляет доступ для запуска скрипта, если это необходимо
RUN chmod a+x /bookforum/docker/*.sh    

# команды выведены в баш-скрипты, чтобы они не прогонялись каждый раз при сборке образа
# они нужны только, если Вы не используете Docker-compose

# RUN alembic upgrade head

# CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]