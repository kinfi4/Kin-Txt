FROM python:3.10

ENV PIP_NO_CACHE_DIR=off \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY ./requirements.txt .

RUN pip install -r requirements.txt
RUN python -c "import nltk; nltk.download('punkt')"

COPY ./kin_generic_builder/ /app/kin_generic_builder
COPY ./submodules/kin-news-core/kin_news_core /app/kin_news_core
