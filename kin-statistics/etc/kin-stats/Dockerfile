FROM python:3.10

ENV PIP_NO_CACHE_DIR=off \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./etc/kin-stats/migrations/ /app/migrations
COPY ./etc/kin-stats/alembic.ini /app/alembic.ini
COPY ./kin_statistics_api/ /app/kin_statistics_api
COPY ./submodules/kin-news-core/kin_news_core /app/kin_news_core

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
