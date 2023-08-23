FROM python:3.10

ENV PIP_NO_CACHE_DIR=off \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./kin_model_types/ /app/kin_model_types
COPY ./submodules/kin-txt-core/kin_news_core /app/kin_news_core
