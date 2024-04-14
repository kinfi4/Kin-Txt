FROM python:3.10

ENV PIP_NO_CACHE_DIR=off \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

WORKDIR /app
COPY ./src/pyproject.toml ./src/poetry.lock* /app/

COPY ./etc/service/migrations/ /app/migrations
COPY ./etc/service/alembic.ini /app/alembic.ini
COPY ./src/kin_statistics_api/ /app/kin_statistics_api
COPY ./submodules /submodules
COPY ./src/tests /app/tests

RUN poetry install
