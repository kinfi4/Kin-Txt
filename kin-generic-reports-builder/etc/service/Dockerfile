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

COPY ./src/kin_generic_builder/ /app/kin_generic_builder
COPY ./submodules /submodules

RUN poetry install
RUN python -c "import nltk; nltk.download('punkt')"
