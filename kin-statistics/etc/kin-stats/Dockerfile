FROM python:3.10

ENV PIP_NO_CACHE_DIR=off \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY ./requirements.txt .

RUN pip install -r requirements.txt
RUN python -c "import nltk; nltk.download('punkt')"

COPY ./kin_statistics_api .
COPY ./submodules/kin-news-core .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
