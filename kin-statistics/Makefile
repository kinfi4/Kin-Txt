UUID = 1000

build:
	docker compose build

run-silent:
	docker compose up -d

run:
	docker compose up

mypy:
	docker compose run -u $(UUID) --rm --no-deps statistics-api mypy kin_statistics_api/

tests:
	docker compose -f docker-compose.test.yaml run --rm statistics-service coverage run -m pytest -vv -s

silent-tests:
	docker compose -f docker-compose.test.yaml run --rm statistics-service coverage run -m pytest -v -q --log-cli-level=CRITICAL

coverage:
	docker compose -f docker-compose.test.yaml run --rm statistics-service coverage report -m

logs:
	docker compose logs -f 

make-migrations:
	docker compose run --rm --no-deps statistics-api alembic revision --autogenerate -m "New migration"
