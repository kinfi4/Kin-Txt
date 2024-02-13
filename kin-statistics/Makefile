UUID = 1000

build:
	docker compose build

run-silent:
	docker compose up -d

run:
	docker compose up

tests:
	docker compose -f docker-compose.test.yaml rm -f postgres mongo
	docker compose -f docker-compose.test.yaml up -d postgres mongo
	docker compose -f docker-compose.test.yaml run --user="root" --rm test-statistics-api python manage.py test api/tests/unit
	docker compose -f docker-compose.test.yaml run --user="root" --rm test-statistics-api python manage.py test api/tests/int
	docker compose -f docker-compose.test.yaml rm -f postgres mongo

mypy:
	docker compose run -u $(UUID) --rm --no-deps statistics-api mypy kin_statistics_api/

tests:
	docker compose -f docker-compose.test.yaml run --rm statistics-service coverage run -m pytest -s

coverage:
	docker compose -f docker-compose.test.yaml run --rm statistics-service coverage report

logs:
	docker compose logs -f 

make-migrations:
	docker compose run --rm --no-deps statistics-api alembic revision --autogenerate -m "New migration"
